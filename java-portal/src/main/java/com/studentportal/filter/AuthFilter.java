package com.studentportal.filter;

import javax.servlet.Filter;
import javax.servlet.FilterChain;
import javax.servlet.FilterConfig;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.annotation.WebFilter;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;

/**
 * Authentication & Authorization Filter.
 * Protects administrative and student record endpoints from unauthenticated access.
 */
@WebFilter(filterName = "AuthFilter", urlPatterns = {"/students", "/profile", "/dashboard"})
public class AuthFilter implements Filter {

    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
    }

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {

        HttpServletRequest req = (HttpServletRequest) request;
        HttpServletResponse resp = (HttpServletResponse) response;

        // Prevent browser caching of protected pages
        resp.setHeader("Cache-Control", "no-cache, no-store, must-revalidate");
        resp.setHeader("Pragma", "no-cache");
        resp.setDateHeader("Expires", 0);

        HttpSession session = req.getSession(false);
        boolean isLoggedIn = (session != null && session.getAttribute("adminUser") != null);

        if (isLoggedIn) {
            chain.doFilter(request, response);
        } else {
            String loginUrl = req.getContextPath() + "/login";
            resp.sendRedirect(loginUrl);
        }
    }

    @Override
    public void destroy() {
    }
}
