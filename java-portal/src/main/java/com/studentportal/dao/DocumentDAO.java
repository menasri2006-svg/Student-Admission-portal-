package com.studentportal.dao;

import com.studentportal.config.DBConnection;
import com.studentportal.model.StudentDocument;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

/**
 * Data Access Object for document metadata retrieval and validation.
 */
public class DocumentDAO {

    /**
     * Finds a document record by its primary key ID.
     *
     * @param id Document ID
     * @return StudentDocument or null if not found
     * @throws SQLException on database error
     */
    public StudentDocument getDocumentById(int id) throws SQLException {
        String sql = "SELECT * FROM student_documents WHERE id = ? LIMIT 1";
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setInt(1, id);
            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
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
        }
        return null;
    }

    /**
     * Finds a document record by its secure stored filename.
     */
    public StudentDocument getDocumentByStoredFilename(String storedFilename) throws SQLException {
        String sql = "SELECT * FROM student_documents WHERE stored_filename = ? LIMIT 1";
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, storedFilename);
            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
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
        }
        return null;
    }
}
