"""Inspect the hardware relevant to local AI inference.

This script intentionally uses the Python standard library where possible.
It does not download a model and it does not require a paid service.
"""

from __future__ import annotations

import ctypes
import json
import platform
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass


GIB = 1024 ** 3


@dataclass
class NvidiaGpu:
    name: str
    vram_gib: float
    driver_version: str


def get_total_ram_gib() -> float | None:
    """Return total system RAM in GiB without requiring psutil."""

    if sys.platform == "win32":
        class MemoryStatusEx(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        status = MemoryStatusEx()
        status.dwLength = ctypes.sizeof(MemoryStatusEx)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
            return status.ullTotalPhys / GIB
        return None

    # Unix-like fallback.
    try:
        page_size = int(__import__("os").sysconf("SC_PAGE_SIZE"))
        page_count = int(__import__("os").sysconf("SC_PHYS_PAGES"))
        return (page_size * page_count) / GIB
    except (AttributeError, ValueError, OSError):
        return None


def get_nvidia_gpus() -> list[NvidiaGpu]:
    """Ask the NVIDIA driver for GPU name, VRAM and driver version."""

    executable = shutil.which("nvidia-smi")
    if executable is None:
        return []

    command = [
        executable,
        "--query-gpu=name,memory.total,driver_version",
        "--format=csv,noheader,nounits",
    ]

    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
    except (subprocess.SubprocessError, OSError):
        return []

    gpus: list[NvidiaGpu] = []

    for line in completed.stdout.splitlines():
        if not line.strip():
            continue

        name, memory_mib, driver_version = [part.strip() for part in line.split(",", 2)]
        gpus.append(
            NvidiaGpu(
                name=name,
                vram_gib=float(memory_mib) / 1024,
                driver_version=driver_version,
            )
        )

    return gpus


def get_torch_info() -> dict[str, object]:
    """Report what PyTorch can see, if PyTorch is installed."""

    try:
        import torch
    except ImportError:
        return {"installed": False}

    info: dict[str, object] = {
        "installed": True,
        "version": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
    }

    if torch.cuda.is_available():
        devices = []
        for index in range(torch.cuda.device_count()):
            props = torch.cuda.get_device_properties(index)
            devices.append(
                {
                    "index": index,
                    "name": props.name,
                    "vram_gib": round(props.total_memory / GIB, 2),
                }
            )
        info["cuda_devices"] = devices

    return info


def main() -> None:
    ram_gib = get_total_ram_gib()
    nvidia_gpus = get_nvidia_gpus()

    report = {
        "python": platform.python_version(),
        "operating_system": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor() or "Not reported by platform",
        "ram_gib": round(ram_gib, 2) if ram_gib is not None else None,
        "nvidia_gpus": [asdict(gpu) for gpu in nvidia_gpus],
        "pytorch": get_torch_info(),
    }

    print("LOCAL AI HARDWARE REPORT")
    print("=" * 60)
    print(json.dumps(report, indent=2))

    print("\nHOW TO READ THIS")
    print("=" * 60)
    print("RAM is system memory available to the operating system and CPU processes.")

    if nvidia_gpus:
        print("An NVIDIA GPU was detected through nvidia-smi.")
        print("VRAM is the dedicated memory available on that GPU.")
    else:
        print("No NVIDIA GPU was detected through nvidia-smi.")
        print("This does not prove that the machine has no GPU; it only means this check did not find an NVIDIA GPU/driver interface.")

    print("PyTorch CUDA availability tells us whether this PyTorch installation can currently use a CUDA-capable NVIDIA GPU.")
    print("A GPU existing in the machine and PyTorch being configured to use it are two different facts.")


if __name__ == "__main__":
    main()
