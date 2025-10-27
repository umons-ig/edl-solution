import org.junit.Test;
import static org.junit.Assert.*;

/**
 * Tests unitaires pour StringUtils
 */
public class StringUtilsTest {

    @Test
    public void testReverse() {
        assertEquals("olleh", StringUtils.reverse("hello"));
        assertEquals("", StringUtils.reverse(""));
    }

    @Test(expected = IllegalArgumentException.class)
    public void testReverseWithNull() {
        StringUtils.reverse(null);
    }

    @Test
    public void testIsPalindrome() {
        assertTrue(StringUtils.isPalindrome("radar"));
        assertTrue(StringUtils.isPalindrome("kayak"));
        assertFalse(StringUtils.isPalindrome("hello"));
        assertTrue(StringUtils.isPalindrome(""));
        assertTrue(StringUtils.isPalindrome("A man a plan a canal Panama"));
    }

    @Test
    public void testCountVowels() {
        assertEquals(2, StringUtils.countVowels("hello"));
        assertEquals(2, StringUtils.countVowels("HELLO"));
        assertEquals(0, StringUtils.countVowels("xyz"));
        assertEquals(0, StringUtils.countVowels(""));
        assertEquals(5, StringUtils.countVowels("aeiou"));
    }

    @Test
    public void testCountWords() {
        assertEquals(2, StringUtils.countWords("hello world"));
        assertEquals(1, StringUtils.countWords("one"));
        assertEquals(0, StringUtils.countWords(""));
        assertEquals(0, StringUtils.countWords("   "));
        assertEquals(3, StringUtils.countWords("one two three"));
    }
}
