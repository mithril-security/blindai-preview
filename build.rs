use std::env;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("cargo:rerun-if-env-changed=BLINDSPEECH_DISALLOW_UPLOAD");
    let disallow_upload_remotely = env::var("BLINDSPEECH_DISALLOW_UPLOAD");
    match disallow_upload_remotely {
        Ok(_) => println!("cargo:rustc-cfg=DISALLOW_UPLOAD_REMOTELY=\"true\""),
        Err(_) => (),
    };
    Ok(())
}