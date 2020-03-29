import java.awt.Color;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.net.URI;
import java.net.URL;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.http.HttpResponse.BodyHandlers;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;
import java.util.Scanner;
import java.util.UUID;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;

import javax.imageio.ImageIO;

/**
CC by SA
https://creativecommons.org/licenses/by-sa/2.0/fr/
*/

public class H25Send_override {


	static int w = 32; // Dimension de l'image
	static int h = 32;
		
	public static void main(String[] args) throws IOException, InterruptedException {
		int dx = 60; // Position sur l'image x
		int dy = 15; // Position sur l'image y

		run(dx, dy);
	}

	static BlockingQueue<String> proofs = new ArrayBlockingQueue<>(100000);

	static class Pt {
		int x, y;
		Color c;
		private int col;

		public Pt(int x, int y, Color c, int col) {
			super();
			this.x = x;
			this.y = y;
			this.c = c;
			this.col = col;
		}

	}

	private static void run(int dx, int dy) throws IOException, InterruptedException {
		read();
		new Thread(() -> compute(), "Hashing").start();

		final InputStream resource = new FileInputStream(new File("./image.png"));
		BufferedImage image = ImageIO.read(resource);


		
		List<Pt> pts = new ArrayList<>();

		for (int i = 0; i < w; i++) {
			for (int j = 0; j < h; j++) {
				Color c = new Color(image.getRGB(i, j));
				if (image.getRGB(i, j) != 0) {
					pts.add(new Pt(i, j, c, image.getRGB(i, j)));
				}
			}
		}

		Collections.shuffle(pts);

		System.out.println(pts.size());
		URL url = new URL("http://137.74.47.86/image");
		BufferedImage current = ImageIO.read(url.openStream());

		Random r = new Random();
		while (true) {
			String proof = proofs.take();
			
			try {
				current = ImageIO.read(url.openStream());
			} catch (IOException e) {
			}
			
			int i = r.nextInt(pts.size());
			Pt p = pts.get(i);
			while (current.getRGB(p.x, p.y) == p.col) {
				i = r.nextInt(pts.size());
				p = pts.get(i);
			}
			send(dx + p.x, dy + p.y, p.c, proof);
		}
	}

	private static void read() {
		InputStream proofsTxt;
		try {
			proofsTxt = new FileInputStream(new File("./proofs.txt"));
			try (var sc = new Scanner(proofsTxt)) {
				while (sc.hasNext()) {
					String nextLine = sc.nextLine();
					String s = nextLine.split(" ")[0];
					proofs.add(s);
				}
			}
		} catch (FileNotFoundException e) {
			// Tant pis pas de hash pre calcules
		}
	}

	private static boolean send(int x, int y, Color color, String proof) throws IOException, InterruptedException {
		HttpClient client = HttpClient.newHttpClient();
		String hex = String.format("#%02x%02x%02x", color.getRed(), color.getGreen(), color.getBlue()).substring(1);
		HttpRequest request = HttpRequest.newBuilder(URI.create("http://137.74.47.86/setpixel?x=" + x + "&y=" + y + "&color=" + hex + "&proof=" + proof)).GET().build();
		HttpResponse<String> send = client.send(request, BodyHandlers.ofString());
		final boolean res = send.statusCode() == 200;
		if (res) {
			System.out.println("ok " + x + " " + y);
		} else {
			System.out.println("ko " + x + " " + y);
		}
		return res;
	}

	private static void compute() {
		try {
			while (true) {
				String originalString = "egaetan" + UUID.randomUUID().toString().replace("-", "");

				String a = extracted(originalString);
				if (a.startsWith("00000")) {
					proofs.add(originalString);
				}

			}
		} catch (NoSuchAlgorithmException e) {
			throw new RuntimeException(e);
		}
	}

	private final static MessageDigest digest = digest();

	private static MessageDigest digest() {
		try {
			return MessageDigest.getInstance("SHA-256");
		} catch (NoSuchAlgorithmException e) {
			throw new RuntimeException(e);
		}

	}

	private static String extracted(String originalString) throws NoSuchAlgorithmException {
		byte[] encodedhash = digest.digest(("h25" + originalString).getBytes(StandardCharsets.UTF_8));

		return bytesToHex(encodedhash);
	}

	private static String bytesToHex(byte[] hash) {
		StringBuffer hexString = new StringBuffer();
		for (int i = 0; i < hash.length; i++) {
			String hex = Integer.toHexString(0xff & hash[i]);
			if (hex.length() == 1)
				hexString.append('0');
			hexString.append(hex);
		}
		return hexString.toString();
	}
}
