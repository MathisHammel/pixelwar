use criterion::{criterion_group, criterion_main, Criterion};
use pixelwar_client_rs::proof;

fn criterion_benchmark(c: &mut Criterion) {
    let mut proof_gen = proof::ProofGeneratorBuilder::new()
            .with_prefix("prefix-")
            .with_suffix_length(20)
            .with_digest_prefix("00000")
            .with_rand_seed(42)
            .build();

    c.bench_function("gen_proof 7 20 00000", |b| b.iter(|| proof_gen.next()));
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
