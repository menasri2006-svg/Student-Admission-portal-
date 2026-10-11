package com.studentportal.dao;

import com.studentportal.config.DBConnection;
import com.studentportal.model.AdminUser;
import com.studentportal.util.BCrypt;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

/**
 * Data Access Object for Administrator authentication and credentials.
 */
public class AdminDAO {

    /**
     * Authenticates administrator credentials using PreparedStatement and BCrypt.
     *
     * @param username admin username
     * @param plainPassword plain-text password from login form
     * @return AdminUser on successful authentication, or null on failure
     * @throws SQLException on database error
     */
    public AdminUser authenticate(String username, String plainPassword) throws SQLException {
        if (username == null || plainPassword == null || username.trim().isEmpty()) {
            return null;
        }

        String sql = "SELECT id, username, password_hash, full_name, email, role FROM admin_users WHERE username = ? LIMIT 1";
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, username.trim());
            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    String hash = rs.getString("password_hash");
                    if (BCrypt.checkpw(plainPassword, hash)) {
                        AdminUser admin = new AdminUser();
                        admin.setId(rs.getInt("id"));
                        admin.setUsername(rs.getString("username"));
                        admin.setPasswordHash(hash);
                        admin.setFullName(rs.getString("full_name"));
                        admin.setEmail(rs.getString("email"));
                        admin.setRole(rs.getString("role"));
                        return admin;
                    }
                }
            }
        }
        return null;
    }
}
