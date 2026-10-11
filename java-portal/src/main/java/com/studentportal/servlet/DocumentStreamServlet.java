package com.studentportal.servlet;

import com.studentportal.dao.DocumentDAO;
import com.studentportal.model.StudentDocument;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.sql.SQLException;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

/**
 * Dedicated secure image and document streaming Servlet.
 * Resolves physical files exclusively via database metadata or validated filenames.
 * Enforces path traversal prevention, content validation, and session authorization.
 */
@WebServlet(name = "DocumentStreamServlet", urlPatterns = {"/document"})
public class DocumentStreamServlet extends HttpServlet {

    private static final Set<String> DISALLOWED_EXTENSIONS = new HashSet<>(Arrays.asList(
        "jsp", "jspx", "class", "java", "php", "phtml", "exe", "bat", "cmd", "sh", "pl", "cgi"
    ));

    private DocumentDAO documentDAO;

    @Override
    public void init() throws ServletException {
        super.init();
        this.documentDAO = new DocumentDAO();
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String idParam = req.getParameter("id");
        String profileParam = req.getParameter("profile");
        boolean forceDownload = "true".equalsIgnoreCase(req.getParameter("download")) || "1".equals(req.getParameter("download"));

        File targetFile = null;
        String mimeType = "application/octet-stream";
        String originalFilename = "document";

        File uploadsBaseDir = resolveUploadsBaseDir();

        if (profileParam != null && !profileParam.trim().isEmpty()) {
            // Streaming profile picture (avatar preview)
            String cleanName = new File(profileParam.trim()).getName();
            if (!cleanName.matches("^[a-zA-Z0-9._-]+$")) {
                resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "Invalid profile image format.");
                return;
            }

            File profileDir = new File(uploadsBaseDir, "profile_images");
            targetFile = new File(profileDir, cleanName);
            originalFilename = cleanName;

            String probed = Files.probeContentType(targetFile.toPath());
            if (probed != null) {
                mimeType = probed;
            } else if (cleanName.toLowerCase().endsWith(".png")) {
                mimeType = "image/png";
            } else if (cleanName.toLowerCase().endsWith(".webp")) {
                mimeType = "image/webp";
            } else {
                mimeType = "image/jpeg";
            }

        } else if (idParam != null && !idParam.trim().isEmpty()) {
            // Private academic documents: require logged-in administrator session
            HttpSession session = req.getSession(false);
            if (session == null || session.getAttribute("adminUser") == null) {
                resp.sendError(HttpServletResponse.SC_UNAUTHORIZED, "Please log in to view or download student documents.");
                return;
            }

            int docId;
            try {
                docId = Integer.parseInt(idParam.trim());
            } catch (NumberFormatException e) {
                resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "Invalid document identifier.");
                return;
            }

            try {
                StudentDocument doc = documentDAO.getDocumentById(docId);
                if (doc == null) {
                    resp.sendError(HttpServletResponse.SC_NOT_FOUND, "Document record not found in system database.");
                    return;
                }

                // Resolve relative path against uploads base directory
                String relPath = doc.getFilePath();
                if (relPath.startsWith("uploads/")) {
                    relPath = relPath.substring("uploads/".length());
                } else if (relPath.startsWith("uploads\\")) {
                    relPath = relPath.substring("uploads\\".length());
                }

                targetFile = new File(uploadsBaseDir, relPath);
                mimeType = doc.getMimeType();
                originalFilename = doc.getOriginalFilename();

            } catch (SQLException e) {
                e.printStackTrace();
                resp.sendError(HttpServletResponse.SC_INTERNAL_SERVER_ERROR, "Database lookup failure.");
                return;
            }

        } else {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "Missing document or profile identifier.");
            return;
        }

        // Security Check 1: Existence check
        if (targetFile == null || !targetFile.exists() || !targetFile.isFile()) {
            resp.sendError(HttpServletResponse.SC_NOT_FOUND, "Requested file does not exist on storage.");
            return;
        }

        // Security Check 2: Path Traversal defense
        String canonicalTarget = targetFile.getCanonicalPath();
        String canonicalBase = uploadsBaseDir.getCanonicalPath();
        if (!canonicalTarget.startsWith(canonicalBase)) {
            resp.sendError(HttpServletResponse.SC_FORBIDDEN, "Access denied: Unauthorized directory traversal attempt.");
            return;
        }

        // Security Check 3: Block execution of active code files
        String ext = getFileExtension(canonicalTarget);
        if (DISALLOWED_EXTENSIONS.contains(ext.toLowerCase())) {
            resp.sendError(HttpServletResponse.SC_FORBIDDEN, "Execution of uploaded scripts is strictly blocked.");
            return;
        }

        // Prepare response headers
        resp.setContentType(mimeType);
        resp.setContentLengthLong(targetFile.length());
        resp.setHeader("X-Content-Type-Options", "nosniff");
        resp.setHeader("Cache-Control", "private, max-age=3600");

        String disposition = forceDownload ? "attachment" : "inline";
        String encodedFilename = URLEncoder.encode(originalFilename, StandardCharsets.UTF_8.toString()).replace("+", "%20");
        resp.setHeader("Content-Disposition", disposition + "; filename=\"" + encodedFilename + "\"");

        // Stream binary data in 8KB chunks
        try (FileInputStream fis = new FileInputStream(targetFile);
             OutputStream os = resp.getOutputStream()) {
            byte[] buffer = new byte[8192];
            int bytesRead;
            while ((bytesRead = fis.read(buffer)) != -1) {
                os.write(buffer, 0, bytesRead);
            }
            os.flush();
        }
    }

    private File resolveUploadsBaseDir() {
        String customPath = System.getenv("UPLOADS_DIR");
        if (customPath != null && !customPath.trim().isEmpty()) {
            File f = new File(customPath.trim());
            if (f.exists()) return f;
        }

        // 1. Direct workspace location
        File wsUploads = new File("E:/Webproject/php-admin/uploads");
        if (wsUploads.exists()) return wsUploads;

        // 2. Relative to Tomcat webapps
        File localHtdocs = new File("C:/xampp/htdocs/student-admission-portal/php-admin/uploads");
        if (localHtdocs.exists()) return localHtdocs;

        // 3. Fallback to webapp uploads directory
        String realPath = getServletContext().getRealPath("/uploads");
        if (realPath != null) {
            File f = new File(realPath);
            if (!f.exists()) f.mkdirs();
            return f;
        }

        return new File("uploads");
    }

    private String getFileExtension(String path) {
        int dot = path.lastIndexOf('.');
        return (dot > 0 && dot < path.length() - 1) ? path.substring(dot + 1) : "";
    }
}
