import com.studentportal.util.BCrypt;

public class TestBCrypt {
    public static void main(String[] args) {
        String hash = "$2y$10$pqlfs4UhUDhaSV2HirlmiOfB2d3UowuIeayCU77dfJzV48AG4U8qG";
        boolean match = BCrypt.checkpw("Password@123", hash);
        System.out.println("Java BCrypt match: " + match);
    }
}
