use core::fmt;
use image::{GenericImageView, Pixel};
use rand::prelude::*;
use rayon::prelude::*;

mod proof;

const CANVAS_W: usize = 100;
const CANVAS_H: usize = 100;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct Color(u8, u8, u8);

impl fmt::Display for Color {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{:x}{:x}{:x}", self.0, self.1, self.2)
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct Pos {
    x: u32,
    y: u32,
}

impl Pos {
    pub fn new(x: u32, y: u32) -> Self {
        Self { x, y }
    }
}

impl core::ops::Add for Pos {
    type Output = Pos;
    fn add(mut self, rhs: Self) -> Self::Output {
        self.x += rhs.x;
        self.y += rhs.y;
        self
    }
}

fn send_pixel(position: Pos, color: Color, proof: &str) {
    let req = format!(
        "http://137.74.47.86/setpixel?x={}&y={}&color={}&proof={}",
        position.x, position.y, color, proof
    );
    let resp = reqwest::blocking::get(&req);

    match resp {
        Ok(_) => log::info!("Ok: {}", req),
        Err(e) => log::warn!("Failed to send:\n - to: {}\n - error: {:#?}", req, e),
    }
}

fn paint(proof_gen: proof::ProofGenerator, pixels: &[(Pos, Color)]) {
    let create_proof_gen = || proof_gen.clone();

    pixels
        .into_par_iter()
        .for_each_with(create_proof_gen(), |proof_gen, (position, color)| {
            let proof = proof_gen.next().unwrap();

            send_pixel(*position, *color, &proof)
        });
}

#[allow(dead_code)]
fn fill_rect(proof_gen: proof::ProofGenerator, top_left: Pos, bottom_right: Pos, color: Color) {
    let mut pixels = Vec::with_capacity(100 * 100);
    for x in top_left.x..bottom_right.x {
        for y in top_left.y..bottom_right.y {
            if x + y % 2 == 0 || x % 2 == 0 {
                pixels.push((Pos::new(99 - x, 99 - y), color));
            }
        }
    }
    let mut rng = rand::thread_rng();
    pixels.shuffle(&mut rng);
    paint(proof_gen, &pixels);
}

// TODO: Make this a struct, builder-based interface
fn paint_image(proof_gen: proof::ProofGenerator, top_left: Pos, image_path: impl AsRef<std::path::Path>) {
    let mut pixels = Vec::with_capacity(CANVAS_W * CANVAS_H);
    let img = image::open(image_path).unwrap();
    let (width, height) = img.dimensions();
    for x in 0..width {
        for y in 0..height {
            let pixel = img.get_pixel(x, y);
            let rgb = pixel.to_rgb();
            let color = Color(rgb.0[0], rgb.0[1], rgb.0[2]);

            if color != Color(255, 0, 0) {
                pixels.push((Pos::new(x, y) + top_left, color));
            }
        }
    }
    let mut rng = rand::thread_rng();
    pixels.shuffle(&mut rng);
    paint(proof_gen, &pixels);
}

fn main() {
    env_logger::init();
    println!("pixelwar.h25.io client from totorigolo.");

    let proof_gen = proof::ProofGeneratorBuilder::new()
            .with_prefix("totorigolo-")
            .with_suffix_length(20)
            .with_digest_prefix("00000")
            .build();

    loop {
        // paint_pink();
        paint_image(proof_gen.clone(), Pos::new(2, 20), "images/insalgo-30-rouge.png");
    }
}
