package com.studentportal.servlet;

import com.studentportal.dao.StudentDAO;
import com.studentportal.model.Student;
import com.studentportal.model.StudentDocument;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.sql.SQLException;
import java.util.List;

/**
 * Retrieves a single student profile and all associated document metadata.
 */
@WebServlet(name = "StudentProfileServlet", urlPatterns = {"/profile"})
public class StudentProfileServlet extends HttpServlet {

    private StudentDAO studentDAO;

    @Override
    public void init() throws ServletException {
        super.init();
        this.studentDAO = new StudentDAO();
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String idParam = req.getParameter("id");
        if (idParam == null || idParam.trim().isEmpty()) {
            resp.sendRedirect(req.getContextPath() + "/students");
            return;
        }

        int studentId;
        try {
            studentId = Integer.parseInt(idParam.trim());
        } catch (NumberFormatException e) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "Invalid student identifier.");
            return;
        }

        try {
            Student student = studentDAO.getStudentById(studentId);
            if (student == null) {
                req.setAttribute("errorMessage", "Student record #" + studentId + " was not found in the database.");
                req.getRequestDispatcher("/WEB-INF/jsp/students.jsp").forward(req, resp);
                return;
            }

            List<StudentDocument> documents = studentDAO.getDocumentsByStudentId(studentId);

            req.setAttribute("student", student);
            req.setAttribute("documents", documents);
            req.getRequestDispatcher("/WEB-INF/jsp/profile.jsp").forward(req, resp);

        } catch (SQLException e) {
            e.printStackTrace();
            resp.sendError(HttpServletResponse.SC_INTERNAL_SERVER_ERROR, "Database failure: " + e.getMessage());
        }
    }
}
