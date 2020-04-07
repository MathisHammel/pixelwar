package bouga.h25;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.security.MessageDigest;

/**
 * Same as App, but with no external lib (for repl.it)
 */
public class Main {

	public static String prefix = "hahaha";
	public static String filename = "proofs_java_2.txt";

	public static int n = 30 - prefix.length();
	public static int[] indexes = new int[n];
	public static String values = "h25io";
	public static boolean done = false;

	public static void main(String[] args) throws IOException {
		try (BufferedWriter writer = new BufferedWriter(new FileWriter(filename, true))) {
			while (!done) {
				String proof = computeProof();
				MessageDigest digest = MessageDigest.getInstance("SHA-256");
				byte[] hashRaw = digest.digest(("h25" + proof).getBytes("UTF-8"));
				String hash= bytesToHex(hashRaw);
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
	
	private static String bytesToHex(byte[] hash) {
	    StringBuffer hexString = new StringBuffer();
	    for (int i = 0; i < hash.length; i++) {
	    String hex = Integer.toHexString(0xff & hash[i]);
	    if(hex.length() == 1) hexString.append('0');
	        hexString.append(hex);
	    }
	    return hexString.toString();
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
