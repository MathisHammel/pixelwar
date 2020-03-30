use sha2::{Digest, Sha256};

pub struct ProofGeneratorBuilder {
    generator: ProofGenerator,
}

impl ProofGeneratorBuilder {
    /// Creates a new `ProofGeneratorBuilder`. You can use `build()` to
    /// obtain an initialized `ProofGenerator.`
    ///
    /// By default, all attributes are empty/zero.
    pub fn new() -> Self {
        Self {
            generator: ProofGenerator {
                prefix: String::new(),
                suffix_length: 0,
                digest_prefix: String::new(),
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

    pub fn build(self) -> ProofGenerator {
        self.generator
    }
}

#[derive(Debug, Clone)]
pub struct ProofGenerator {
    prefix: String,
    suffix_length: usize,
    digest_prefix: String,
}

impl Iterator for ProofGenerator {
    type Item = String;

    fn next(&mut self) -> Option<Self::Item> {
        // TODO: Try smallstring
        // TODO: use Sha256::reset
        // TODO: Bench unsafe vs. unwrap

        loop {
            let proof_suffix = (0..self.suffix_length)
                .map(|_| rand::random::<u8>())
                .map(|x| x % 26 + b'a')
                .collect();
            // Safety: only lowercase letters
            let proof_suffix = unsafe { String::from_utf8_unchecked(proof_suffix) };

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
