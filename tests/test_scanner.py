from src.scanner import scan_network, fingerprint_device

def test_scan_network_runs():
    devices = scan_network("192.168.1.0/24")
    assert isinstance(devices, list)

def test_fingerprint_unknown():
    result = fingerprint_device("127.0.0.1")
    assert isinstance(result, str)
