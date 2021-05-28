package case1;
import java.util.Scanner;

public class Main {
    static double circleArea(double r) {
        return Math.PI * Math.pow(r, 2);
    }

    public static void main(String[] args) {
        System.out.println("Please enter the radius of the circle: ");
        var scanner = new Scanner(System.in);
        var r = scanner.nextDouble();
        if (r <= 0) {
            System.out.println("Circle radius must be positive");
        } else {
            var res = circleArea(r);
            System.out.printf("Circle area: %.2f", res);
        }
        scanner.close();
    }
}