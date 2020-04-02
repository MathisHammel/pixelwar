use pixelwar_client_rs::{Pos, proof, paint_image};

fn main() {
    env_logger::init();
    println!("pixelwar.h25.io client from totorigolo.");

    let proof_gen = proof::ProofGeneratorBuilder::new()
            .with_prefix("totorigolo-")
            .with_suffix_length(24)
            .with_digest_prefix("00000")
            .build();

    loop {
        // paint_pink();
        paint_image(proof_gen.clone(), Pos::new(100 - 35, 100 - 35), "images/insalgo-30-rouge.png");
    }
}
