package com.studentportal.servlet;

import com.studentportal.dao.StudentDAO;
import com.studentportal.model.Student;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.sql.SQLException;
import java.util.List;
import java.util.Map;

/**
 * Retrieves and lists registered students from the database.
 * Supports keyword search, metrics aggregation, and forwards to JSP view.
 */
@WebServlet(name = "StudentListServlet", urlPatterns = {"/students", "/dashboard"})
public class StudentListServlet extends HttpServlet {

    private StudentDAO studentDAO;

    @Override
    public void init() throws ServletException {
        super.init();
        this.studentDAO = new StudentDAO();
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String search = req.getParameter("search");

        try {
            List<Student> students = studentDAO.getAllStudents(search);
            int totalStudents = studentDAO.getTotalStudents();
            int totalDocs = studentDAO.getTotalDocuments();
            Map<String, Integer> courseSummary = studentDAO.getCourseSummary();

            req.setAttribute("students", students);
            req.setAttribute("totalStudents", totalStudents);
            req.setAttribute("totalDocs", totalDocs);
            req.setAttribute("courseSummary", courseSummary);
            req.setAttribute("searchQuery", (search != null) ? search.trim() : "");

            req.getRequestDispatcher("/WEB-INF/jsp/students.jsp").forward(req, resp);
        } catch (SQLException e) {
            e.printStackTrace();
            req.setAttribute("dbError", "Database error while fetching student records: " + e.getMessage());
            req.getRequestDispatcher("/WEB-INF/jsp/students.jsp").forward(req, resp);
        }
    }
}
