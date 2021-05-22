package case9;
import java.util.Scanner;

public class Main {
    static double circleArea(double r = 6) {
        return Math.PI * Math.pow(r, 2);
    }

    public static void main(String[] args) {
        var scanner = new Scanner(System.in);
        var r = scanner.nextDouble() // missing ; here
        int a;
        int b;
        int c;
        int d;
        in z = a + (c + d); // typo here
        if (r <= 0) {
            System.out.println("Circle radius must be positive");
        } else {
            var res = circleArea(r);
            System.out.printf("Circle area: %.2f", res);
        }
        scanner.close();
    }
}