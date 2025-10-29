/**
 * Classe Perimetre - Calcul de périmètre ((a + b) * c)
 * SOLUTION COMPLÈTE
 */
public class Perimetre {

    /**
     * Calculer le périmètre
     * Formule: (a + b) * c
     */
    public static int perim(int a, int b, int c) {
        int somme = Addition.add(a, b);
        return Produit.mult(somme, c);
    }
}
