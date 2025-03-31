import testinfra
import pytest

def test_os_release(host):
    os_release = host.file("/etc/os-release")
    assert os_release.exists
    assert 'ubuntu' in os_release.content_string.lower()



def test_package_is_installed(host):
    package_name = "nginx"
    package = host.package(package_name)
    assert package.is_installed, f"{package_name} is not installed."


def test_process_is_running(host):
    process_name = "salt"
    processes = host.process.filter(comm=process_name)
    assert len(processes) > 0, f"No running processes found for {process_name}"