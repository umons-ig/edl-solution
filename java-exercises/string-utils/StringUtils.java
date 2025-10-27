/**
 * Classe StringUtils - Manipulation de chaînes
 * Exercice : Implémenter les méthodes et écrire les tests
 */
public class StringUtils {

    public static String reverse(String str) {
        if (str == null) {
            throw new IllegalArgumentException("String cannot be null");
        }
        return new StringBuilder(str).reverse().toString();
    }

    public static boolean isPalindrome(String str) {
        if (str == null) {
            throw new IllegalArgumentException("String cannot be null");
        }
        String cleaned = str.toLowerCase().replaceAll("\\s+", "");
        return cleaned.equals(new StringBuilder(cleaned).reverse().toString());
    }

    public static int countVowels(String str) {
        if (str == null) {
            throw new IllegalArgumentException("String cannot be null");
        }
        int count = 0;
        String vowels = "aeiouAEIOU";
        for (int i = 0; i < str.length(); i++) {
            if (vowels.indexOf(str.charAt(i)) != -1) {
                count++;
            }
        }
        return count;
    }

    public static int countWords(String str) {
        if (str == null) {
            throw new IllegalArgumentException("String cannot be null");
        }
        if (str.trim().isEmpty()) {
            return 0;
        }
        String[] words = str.trim().split("\\s+");
        return words.length;
    }
}
