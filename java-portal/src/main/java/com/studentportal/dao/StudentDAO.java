package com.studentportal.dao;

import com.studentportal.config.DBConnection;
import com.studentportal.model.Student;
import com.studentportal.model.StudentDocument;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Data Access Object for Student and Document retrieval.
 * Connects to the shared database schema using PreparedStatement and try-with-resources.
 */
public class StudentDAO {

    /**
     * Retrieves all student records, with optional filtering by name or roll number.
     * Includes the count of uploaded documents for each student.
     *
     * @param search optional query to match name or roll_number
     * @return List of Student objects
     * @throws SQLException on database query failure
     */
    public List<Student> getAllStudents(String search) throws SQLException {
        List<Student> list = new ArrayList<>();
        String sql;
        boolean hasSearch = (search != null && !search.trim().isEmpty());

        if (hasSearch) {
            sql = "SELECT s.*, "
                + "  (SELECT COUNT(*) FROM student_documents d WHERE d.student_id = s.id) AS doc_count "
                + "FROM students s "
                + "WHERE s.name LIKE ? OR s.roll_number LIKE ? OR s.course LIKE ? "
                + "ORDER BY s.registration_date DESC";
        } else {
            sql = "SELECT s.*, "
                + "  (SELECT COUNT(*) FROM student_documents d WHERE d.student_id = s.id) AS doc_count "
                + "FROM students s "
                + "ORDER BY s.registration_date DESC";
        }

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            if (hasSearch) {
                String pattern = "%" + search.trim() + "%";
                ps.setString(1, pattern);
                ps.setString(2, pattern);
                ps.setString(3, pattern);
            }

            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    Student s = mapStudent(rs);
                    s.setDocumentCount(rs.getInt("doc_count"));
                    list.add(s);
                }
            }
        }
        return list;
    }

    /**
     * Retrieves a single student by primary key ID.
     *
     * @param id Student ID
     * @return Student or null if not found
     * @throws SQLException on database error
     */
    public Student getStudentById(int id) throws SQLException {
        String sql = "SELECT * FROM students WHERE id = ? LIMIT 1";
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setInt(1, id);
            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    return mapStudent(rs);
                }
            }
        }
        return null;
    }

    /**
     * Retrieves all document records uploaded for a student.
     *
     * @param studentId Student ID
     * @return List of StudentDocument instances
     * @throws SQLException on database error
     */
    public List<StudentDocument> getDocumentsByStudentId(int studentId) throws SQLException {
        List<StudentDocument> docs = new ArrayList<>();
        String sql = "SELECT * FROM student_documents WHERE student_id = ? ORDER BY uploaded_at DESC";
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setInt(1, studentId);
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    docs.add(mapDocument(rs));
                }
            }
        }
        return docs;
    }

    /**
     * Returns total registered student count.
     */
    public int getTotalStudents() throws SQLException {
        String sql = "SELECT COUNT(*) FROM students";
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            if (rs.next()) {
                return rs.getInt(1);
            }
        }
        return 0;
    }

    /**
     * Returns total uploaded document count.
     */
    public int getTotalDocuments() throws SQLException {
        String sql = "SELECT COUNT(*) FROM student_documents";
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            if (rs.next()) {
                return rs.getInt(1);
            }
        }
        return 0;
    }

    /**
     * Returns student count grouped by course program.
     */
    public Map<String, Integer> getCourseSummary() throws SQLException {
        Map<String, Integer> map = new LinkedHashMap<>();
        String sql = "SELECT course, COUNT(*) AS cnt FROM students GROUP BY course ORDER BY cnt DESC";
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                map.put(rs.getString("course"), rs.getInt("cnt"));
            }
        }
        return map;
    }

    private Student mapStudent(ResultSet rs) throws SQLException {
        Student s = new Student();
        s.setId(rs.getInt("id"));
        s.setRollNumber(rs.getString("roll_number"));
        s.setName(rs.getString("name"));
        s.setEmail(rs.getString("email"));
        s.setCourse(rs.getString("course"));
        s.setPasswordHash(rs.getString("password_hash"));
        s.setProfileImage(rs.getString("profile_image"));
        s.setStatus(rs.getString("status"));
        s.setRegistrationDate(rs.getTimestamp("registration_date"));
        s.setUpdatedAt(rs.getTimestamp("updated_at"));
        return s;
    }

    private StudentDocument mapDocument(ResultSet rs) throws SQLException {
        StudentDocument d = new StudentDocument();
        d.setId(rs.getInt("id"));
        d.setStudentId(rs.getInt("student_id"));
        d.setOriginalFilename(rs.getString("original_filename"));
        d.setStoredFilename(rs.getString("stored_filename"));
        d.setFilePath(rs.getString("file_path"));
        d.setMimeType(rs.getString("mime_type"));
        d.setFileSize(rs.getLong("file_size"));
        d.setDocumentCategory(rs.getString("document_category"));
        d.setUploadedAt(rs.getTimestamp("uploaded_at"));
        return d;
    }
}
