use core::fmt;
use image::{GenericImageView, Pixel};
use rand::prelude::*;
use rayon::prelude::*;

mod proof;

struct Color(u8, u8, u8);

impl fmt::Display for Color {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{:x}{:x}{:x}", self.0, self.1, self.2)
    }
}

fn send_pixel(x: u32, y: u32, color: &Color, proof: &String) {
    let req = format!(
        "http://137.74.47.86/setpixel?x={}&y={}&color={}&proof={}",
        x, y, color, proof
    );
    let resp = reqwest::blocking::get(&req);

    match resp {
        Ok(_) => log::info!("Ok: {}", req),
        Err(e) => log::warn!("Failed to send:\n - to: {}\n - error: {:#?}", req, e),
    }
}

fn paint(pixels: &[(u32, u32, Color)]) {
    let create_proof_gen = || {
        proof::ProofGeneratorBuilder::new()
            .with_prefix("totorigolo-")
            .with_suffix_length(20)
            .with_digest_prefix("00000")
            .build()
    };

    pixels
        .into_par_iter()
        .for_each_with(create_proof_gen(), |proof_gen, (x, y, color)| {
            let proof = proof_gen.next().unwrap();

            send_pixel(*x, *y, &color, &proof)
        });
}

#[allow(dead_code)]
fn paint_pink() {
    let mut pixels = Vec::with_capacity(100 * 100);
    for x in 0..99 {
        for y in 0..99 {
            if x + y % 2 == 0 || x % 2 == 0 {
                let color = Color(61, 66, 170);
                pixels.push((99 - x, 99 - y, color));
            }
        }
    }
    let mut rng = rand::thread_rng();
    pixels.shuffle(&mut rng);
    paint(&pixels);
}

fn paint_insalgo() {
    let mut pixels = Vec::with_capacity(100 * 100);
    let img = image::open("images/insalgo-30-rouge.png").unwrap();
    let (width, height) = img.dimensions();
    for x in 0..width {
        for y in 0..height {
            let pixel = img.get_pixel(x, y);
            let rgb = pixel.to_rgb();
            let color = Color(rgb.0[0], rgb.0[1], rgb.0[2]);

            if color.0 != 255 {
                pixels.push((x + 2, 99 - (30 + 10) + y, color));
            }
        }
    }
    let mut rng = rand::thread_rng();
    pixels.shuffle(&mut rng);
    paint(&pixels);
}

fn main() {
    env_logger::init();
    println!("pixelwar.h25.io client from totorigolo.");
    loop {
        // paint_pink();
        paint_insalgo();
    }
}
