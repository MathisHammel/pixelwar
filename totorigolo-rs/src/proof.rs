use sha2::{Digest, Sha256};
use rand::{Rng, SeedableRng};
use rand::rngs::SmallRng;

pub struct ProofGeneratorBuilder {
    generator: ProofGenerator,
}

impl ProofGeneratorBuilder {
    /// Creates a new `ProofGeneratorBuilder`. You can use `build()` to
    /// obtain an initialized `ProofGenerator.`
    ///
    /// By default, all attributes are empty/zero.
    #[allow(clippy::new_without_default)]
    pub fn new() -> Self {
        Self {
            generator: ProofGenerator {
                prefix: String::new(),
                suffix_length: 0,
                digest_prefix: String::new(),
                rng: SmallRng::from_entropy(),
            },
        }
    }

    pub fn with_prefix(mut self, prefix: impl ToString) -> ProofGeneratorBuilder {
        self.generator.prefix = prefix.to_string();
        self
    }

    pub fn with_suffix_length(mut self, suffix_length: usize) -> ProofGeneratorBuilder {
        self.generator.suffix_length = suffix_length;
        self
    }

    pub fn with_digest_prefix(mut self, digest_prefix: impl ToString) -> ProofGeneratorBuilder {
        self.generator.digest_prefix = digest_prefix.to_string();
        self
    }

    pub fn with_rand_seed(mut self, seed: u64) -> ProofGeneratorBuilder {
        self.generator.rng = SmallRng::seed_from_u64(seed);
        self
    }

    pub fn build(self) -> ProofGenerator {
        self.generator
    }
}

#[derive(Debug, Clone)]
pub struct ProofGenerator {
    prefix: String,
    suffix_length: usize,
    digest_prefix: String,
    rng: SmallRng,
}

impl Iterator for ProofGenerator {
    type Item = String;

    fn next(&mut self) -> Option<Self::Item> {
        let mut proof_suffix = String::with_capacity(self.suffix_length);

        loop {
            proof_suffix.clear();
            proof_suffix.extend((0..self.suffix_length)
                .map(|_| self.rng.gen::<u8>())
                .map(|x| (x % 26 + b'a') as char));

            let hash = Sha256::new()
                .chain("h25")
                .chain(&self.prefix)
                .chain(&proof_suffix)
                .result();

            if format!("{:x}", hash).starts_with(&self.digest_prefix) {
                let proof = format!("{}{}", self.prefix, proof_suffix);
                log::debug!("Found proof: {} -> {:x}", proof, hash);
                return Some(proof);
            }
        }
    }
}
