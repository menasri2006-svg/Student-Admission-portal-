package com.studentportal.config;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

/**
 * Reusable JDBC Connection Factory for Student Admission Portal.
 * Connects to the shared MySQL/MariaDB database: student_portal.
 */
public class DBConnection {

    private static final String DEFAULT_HOST = "127.0.0.1";
    private static final String DEFAULT_PORT = "3306";
    private static final String DEFAULT_DATABASE = "student_portal";
    private static final String DEFAULT_USER = "root";
    private static final String DEFAULT_PASSWORD = "";

    private static String url;
    private static String user;
    private static String password;

    static {
        String host = System.getenv("DB_HOST") != null ? System.getenv("DB_HOST") : DEFAULT_HOST;
        String port = System.getenv("DB_PORT") != null ? System.getenv("DB_PORT") : DEFAULT_PORT;
        String db = System.getenv("DB_NAME") != null ? System.getenv("DB_NAME") : DEFAULT_DATABASE;
        user = System.getenv("DB_USER") != null ? System.getenv("DB_USER") : DEFAULT_USER;
        password = System.getenv("DB_PASS") != null ? System.getenv("DB_PASS") : DEFAULT_PASSWORD;

        url = "jdbc:mysql://" + host + ":" + port + "/" + db 
            + "?useUnicode=true&characterEncoding=utf8&useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC";

        // Try modern MySQL CJ driver first, fallback to legacy MySQL driver
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
        } catch (ClassNotFoundException e1) {
            try {
                Class.forName("com.mysql.jdbc.Driver");
            } catch (ClassNotFoundException e2) {
                try {
                    Class.forName("org.mariadb.jdbc.Driver");
                } catch (ClassNotFoundException e3) {
                    System.err.println("Notice: JDBC Driver not pre-loaded via Class.forName; relying on DriverManager service loader.");
                }
            }
        }
    }

    /**
     * Obtains a new database connection.
     *
     * @return active java.sql.Connection
     * @throws SQLException if a database access error occurs
     */
    public static Connection getConnection() throws SQLException {
        try {
            return DriverManager.getConnection(url, user, password);
        } catch (SQLException primaryEx) {
            // Automatic resilience: If port 3306 fails, fallback to 3307 (or vice-versa)
            if (url.contains(":3306/")) {
                String fallbackUrl = url.replace(":3306/", ":3307/");
                try {
                    Connection conn = DriverManager.getConnection(fallbackUrl, user, password);
                    url = fallbackUrl;
                    return conn;
                } catch (SQLException fallbackEx) {
                    throw primaryEx;
                }
            } else if (url.contains(":3307/")) {
                String fallbackUrl = url.replace(":3307/", ":3306/");
                try {
                    Connection conn = DriverManager.getConnection(fallbackUrl, user, password);
                    url = fallbackUrl;
                    return conn;
                } catch (SQLException fallbackEx) {
                    throw primaryEx;
                }
            }
            throw primaryEx;
        }
    }

    /**
     * Safely closes one or more JDBC resources without throwing checked exceptions.
     *
     * @param resources AutoCloseable instances (Connection, Statement, ResultSet)
     */
    public static void close(AutoCloseable... resources) {
        if (resources != null) {
            for (AutoCloseable res : resources) {
                if (res != null) {
                    try {
                        res.close();
                    } catch (Exception ignored) {
                    }
                }
            }
        }
    }
}
