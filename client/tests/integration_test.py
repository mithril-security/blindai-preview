import blindai_preview

# response = client_v2.upload_model(model=model_path)
# run_response = client_v2.run_model(model_id=response.model_id, input_tensors=inputs, sign=False)
# client_v2.delete_model(model_id = response.model_id)


def test_connect():
    client = blindai_preview.connect(addr="localhost", simulation=True)