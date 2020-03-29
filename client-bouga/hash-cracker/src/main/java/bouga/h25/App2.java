package bouga.h25;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

import org.apache.commons.codec.digest.DigestUtils;

public class App2 {

	public static String prefix = "gologolo";
	public static String filename = "C:\\Users\\Valentin\\Code\\h25\\proofs_java_2.txt";

	public static int n = 30 - prefix.length();
	public static int[] indexes = new int[n];
	public static String values = "h25io";
	public static boolean done = false;

	public static void main(String[] args) throws IOException {
		try (BufferedWriter writer = new BufferedWriter(new FileWriter(filename, true))) {
			while (!done) {
				String proof = computeProof();
				String hash = DigestUtils.sha256Hex("h25" + proof);
				if (hash.startsWith("00000")) {
					System.out.println(proof);
					writer.write(proof);
					writer.newLine();
					writer.flush();
				}
				bumpIndexes();
			}
		} catch (Exception e) {
			System.err.println("Crashed: " + e.getMessage());
			System.err.println(e);
		}
	}

	public static String computeProof() {
		StringBuilder sb = new StringBuilder(n);
		for (int i = 0; i < n; ++i) {
			sb.append(values.charAt(indexes[i]));
		}
		return prefix + sb.toString();
	}

	public static void bumpIndexes() {
		for (int i = n - 1; i >= 0; --i) {
			if (indexes[i] == values.length() - 1) {
				indexes[i] = 0;
			} else {
				indexes[i]++;
				return;
			}
		}
		done = true;
	}
}
