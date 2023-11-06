import java.util.concurrent.Semaphore;

public class test {

    // Constants
    static final String [] nom_sospitosos = new String[20];
    static final int SOSPITOSOS = 20;

    // Semàfors
    static Semaphore sem_decisio = new Semaphore(0);
    static Semaphore sem_fitxar = new Semaphore(1);
    static Semaphore sem_porta = new Semaphore(1);
    static Semaphore sem_declaracio = new Semaphore(0);
    static Semaphore sem_espera_fitxats = new Semaphore(0);
    static Semaphore sem_veredicte = new Semaphore(0);

    // Counters
    static int counter_fitxats = 0;
    static int counter_sospitosos_sala = 0;
    static int counter_declaracions = 0;

    // Variables
    static boolean veredicte = false;
    // static boolean jutge = false;

    public static void main(String[] args) {
        valor_array_nom_sospitosos();
        for (int i = 0; i < SOSPITOSOS; i++) {
            Sospitoso sospitoso = new Sospitoso(nom_sospitosos[i]);
            sospitoso.start();
        }
        Jutge jutge = new Jutge();
        jutge.start();
    }

    static class Sospitoso extends Thread {
        private String nombre;

        public Sospitoso(String nombre) {
            this.nombre = nombre;
        }

        public void run() {
            System.out.println(nombre + ": Som innocent!");
            try {
                // SALA
                sem_porta.acquire(); // Intenta entrar a la sala
                if (!veredicte) {
                    counter_sospitosos_sala++;
                    System.out.println(nombre + " entra al jutjat. Sospitosos: " + counter_sospitosos_sala);
                    Thread.sleep(100);
                    sem_porta.release(); // Allibera la porta

                    // FITXAR
                    sem_fitxar.acquire(); // Espera a la màquina de fitxar
                    counter_fitxats++;
                    System.out.println(nombre + " fitxa. Fitxats: " + counter_fitxats);
                    Thread.sleep(100);
                    sem_fitxar.release(); // Allibera la màquina de fitxar

                    if (counter_fitxats == counter_sospitosos_sala) {
                        sem_espera_fitxats.release(); // S'avisa al jutge que han fitxat tots
                    }
                    /*
                    sem_jutge.acquire(); // Espera al jutge

                    // DECLARACIÓ
                    sem_declaracio.acquire(); // Espera per declarar
                    counter_declaracions++;
                    System.out.println(nombre + " declara. Declaracions: " + counter_declaracions);
                    sem_decisio.release(); // S'avisa al jutge que ha declarat
                    System.out.println(nombre + " se va");
                    sem_decisio.acquire(); // Espera la decisió del jutge
                    sem_declaracio.release(); // Allibera l'atenció del jutge
                    */
                    // DECLARACIÓ v2
                    sem_declaracio.acquire(); // Espera per declarar
                    counter_declaracions++;
                    System.out.println(nombre + " declara. Declaracions: " + counter_declaracions);
                    Thread.sleep(100);
                    sem_declaracio.release(); // Allibera l'atenció del jutge
                    if (counter_declaracions == counter_fitxats) {
                        sem_decisio.release(); // S'avisa al jutge que han declarat tots
                    }

                    sem_veredicte.acquire(); // Espera el veredicte
                    System.out.println(nombre + " entra a l'asil d'Arkham");
                    Thread.sleep(100);
                } else {
                    System.out.println(nombre + ": No és just vull declarar! Som innocent!");
                    Thread.sleep(100);
                    sem_porta.release(); // Allibera la porta
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }

    static class Jutge extends Thread {
        public void run() {
            System.out.println("----> Jutge Dredd: Jo som la llei!");

            try {
                sem_porta.acquire(); // Tanca la porta
                System.out.println("----> Jutge Dredd: Som a la sala, tanqueu porta!");
                Thread.sleep(100);
                if (counter_sospitosos_sala != 0) {
                    System.out.println("----> Jutge Dredd: Fitxeu als sospitosos presents");
                    Thread.sleep(100);
                    sem_espera_fitxats.acquire(); // Espera que fitxin tots els sospitosos
                    System.out.println("----> Jutge Dredd: Preniu declaració als presents");
                    Thread.sleep(100);
                    /*
                    // DECISIÓ
                    while (counter_declaracions != counter_fitxats) {
                        sem_jutge.release(); // Jutge preparat
                        // Espera la declaració
                        System.out.println("jutge espera declaracio");
                        sem_decisio.acquire();
                        // Decideix
                        sem_decisio.release();
                    }
                    */
                    // DECLARACIONS
                    sem_declaracio.release();

                    // VEREDICTE
                    sem_decisio.acquire();
                    veredicte = true;
                    System.out.println("----> Jutge Dredd: Podeu abandonar la sala tots a l'asil!");
                    Thread.sleep(100);
                    while (counter_sospitosos_sala != 0) {
                        sem_veredicte.release();
                        counter_sospitosos_sala--;
                    }
                } else {
                    veredicte = true;
                    System.out.println("----> Jutge Dredd: Si no hi ha ningú me'n vaig!");
                    Thread.sleep(100);
                }
                sem_porta.release(); // Allibera la porta
                System.out.println("----> Jutge Dredd: La justícia descansa, prendré declaració als sospitosos que queden");
                Thread.sleep(100);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }

    public static void valor_array_nom_sospitosos() {
        nom_sospitosos[0] = "Deadshot";
        nom_sospitosos[1] = "Harley Quinn";
        nom_sospitosos[2] = "Penguin";
        nom_sospitosos[3] = "Riddler";
        nom_sospitosos[4] = "Bane";
        nom_sospitosos[5] = "Talia al Ghul";
        nom_sospitosos[6] = "Ra's al Ghul";
        nom_sospitosos[7] = "Hugo Strange";
        nom_sospitosos[8] = "Killer Croc";
        nom_sospitosos[9] = "Catwoman";
        nom_sospitosos[10] = "Poison Ivy";
        nom_sospitosos[11] = "Mr. Freeze";
        nom_sospitosos[12] = "Jason Todd";
        nom_sospitosos[13] = "Hush";
        nom_sospitosos[14] = "Joker";
        nom_sospitosos[15] = "Clayface";
        nom_sospitosos[16] = "Deathstroke";
        nom_sospitosos[17] = "Mad Hatter";
        nom_sospitosos[18] = "Two-Face";
        nom_sospitosos[19] = "Scarecrow";
    }

}
