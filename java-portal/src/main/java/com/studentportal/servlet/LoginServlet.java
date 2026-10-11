package com.studentportal.servlet;

import com.studentportal.dao.AdminDAO;
import com.studentportal.model.AdminUser;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;
import java.sql.SQLException;

/**
 * Handles administrator authentication into the Java Portal.
 */
@WebServlet(name = "LoginServlet", urlPatterns = {"/login"})
public class LoginServlet extends HttpServlet {

    private AdminDAO adminDAO;

    @Override
    public void init() throws ServletException {
        super.init();
        this.adminDAO = new AdminDAO();
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        HttpSession session = req.getSession(false);
        if (session != null && session.getAttribute("adminUser") != null) {
            resp.sendRedirect(req.getContextPath() + "/students");
            return;
        }

        if ("1".equals(req.getParameter("logout"))) {
            req.setAttribute("successMessage", "You have been safely logged out.");
        }

        req.getRequestDispatcher("/WEB-INF/jsp/login.jsp").forward(req, resp);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        req.setCharacterEncoding("UTF-8");
        String username = req.getParameter("username");
        String password = req.getParameter("password");

        if (username == null || username.trim().isEmpty() || password == null || password.isEmpty()) {
            req.setAttribute("errorMessage", "Please provide both username and password.");
            req.setAttribute("username", username);
            req.getRequestDispatcher("/WEB-INF/jsp/login.jsp").forward(req, resp);
            return;
        }

        try {
            AdminUser admin = adminDAO.authenticate(username, password);
            if (admin != null) {
                // Invalidate old session to prevent session fixation attacks
                HttpSession oldSession = req.getSession(false);
                if (oldSession != null) {
                    oldSession.invalidate();
                }

                // Create fresh session
                HttpSession newSession = req.getSession(true);
                newSession.setAttribute("adminUser", admin);
                newSession.setMaxInactiveInterval(1800); // 30 minutes session timeout

                resp.sendRedirect(req.getContextPath() + "/students");
            } else {
                req.setAttribute("errorMessage", "Invalid administrator username or password.");
                req.setAttribute("username", username);
                req.getRequestDispatcher("/WEB-INF/jsp/login.jsp").forward(req, resp);
            }
        } catch (SQLException e) {
            e.printStackTrace();
            req.setAttribute("errorMessage", "Database error: Could not verify credentials. Verify MySQL service is active.");
            req.getRequestDispatcher("/WEB-INF/jsp/login.jsp").forward(req, resp);
        }
    }
}
