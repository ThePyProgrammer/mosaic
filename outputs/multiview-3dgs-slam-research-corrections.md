# Corrections: Open-Source 3DGS SLAM Systems

Date: 2026-05-18

## Key corrections

1. **RTG-SLAM does have a public repository.** The official-looking repository is `MisEty/RTG-SLAM`, linked from the project page and described as the "official authors implementation". GitHub detects **GPL-3.0** and the repository has a GPLv3 license file.
2. **GS-SLAM public code appears to be only project-page plus modified rasterizer code, not a full SLAM implementation.** The linked repository is explicitly a modified differential Gaussian rasterizer for GS-SLAM. I did not find a full public GS-SLAM implementation in the primary project links.
3. **VIGS-SLAM and VINGS-Mono are different systems.** VIGS-SLAM is a CVG project page pointing to `github.com/cvg/vigs-slam`, but that repository is currently inaccessible/404 via GitHub API. A separate `ghPak1002/VIGS_SLAM` repository says code is temporarily withheld pending acceptance. VINGS-Mono is a Fudan MAGIC Lab TRO 2025 system with public code at `Fudan-MAGIC-Lab/VINGS-Mono`.
4. **Google Splat-SLAM and Erik Sandström Splat-SLAM are the same code line, not two independent systems.** Erik Sandström's repo says the code is now publicly available at `google-research/Splat-SLAM`; the Google Research repo contains the implementation and is Apache-2.0 licensed.
5. **License risk is higher than a simple “open source” label suggests.** Permissive: SplaTAM BSD-3-Clause, Gaussian-SLAM MIT, Google Splat-SLAM Apache-2.0. GPL/copyleft: Photo-SLAM GPLv3, RTG-SLAM GPLv3, Gaussian-LIC GPLv3 per README. Non-commercial/custom/research-only: MonoGS, GS-SLAM rasterizer, DiskChunGS.

## Correction table

| Claim | Status | Corrected wording | Evidence/source refs |
|---|---:|---|---|
| RTG-SLAM has no public code / code was not seen. | Corrected | RTG-SLAM has a public GitHub repository at `MisEty/RTG-SLAM`; the project page links it, the README says it contains the official authors implementation, and it includes setup/run commands. | [1], [2], [3] |
| RTG-SLAM license is unknown. | Corrected | RTG-SLAM is GPL-3.0 according to GitHub license metadata and its `LICENSE` file. | [2], [4] |
| GS-SLAM has a full public implementation. | Corrected | Primary public code found for CVPR 2024 GS-SLAM is a modified differential Gaussian rasterizer, not the full SLAM system. The project page labels the code as “Modified Rasterization Code”; the linked repository describes itself as a modified rasterization version. | [5], [6], [7] |
| GS-SLAM has no public code at all. | Corrected | GS-SLAM has public project-page code and a modified rasterizer repository, but not a full public SLAM implementation from the sources found. | [5], [6], [7] |
| VIGS-SLAM and VINGS-Mono are the same system/name variant. | Corrected | Treat them as different systems. VIGS-SLAM is “Visual Inertial Gaussian Splatting SLAM” with a CVG project page and an inaccessible `cvg/vigs-slam` code link; VINGS-Mono is “Visual-Inertial Gaussian Splatting Monocular SLAM in Large Scenes” with public Fudan MAGIC Lab source code. | [8], [9], [10], [11], [12] |
| VIGS-SLAM has public code. | Unverified / likely not currently accessible | The VIGS-SLAM project page links `https://github.com/cvg/vigs-slam`, but GitHub returns 404 via API. A separate `ghPak1002/VIGS_SLAM` repo says the complete codebase will be released after paper acceptance and is currently withheld. | [8], [10], [11] |
| VINGS-Mono has public code. | Confirmed | VINGS-Mono has public source code at `Fudan-MAGIC-Lab/VINGS-Mono`, created 2025-09-29, with README clone/setup instructions and arXiv/TRO 2025 identification. No license is detected by GitHub. | [9], [12] |
| Google Splat-SLAM and Erik Sandström Splat-SLAM are separate systems. | Corrected | Erik Sandström’s repository is a pointer/staging repo; it says the code is now public at `google-research/Splat-SLAM`. The Google Research repo is the implementation for “Splat-SLAM: Globally Optimized RGB-only SLAM with 3D Gaussians.” | [13], [14], [15] |
| Google Splat-SLAM license is unknown. | Corrected | `google-research/Splat-SLAM` is Apache-2.0 licensed according to GitHub metadata and its license file. | [14], [16] |
| SplaTAM license is unknown. | Corrected | SplaTAM is BSD-3-Clause according to GitHub metadata and its license file. | [17], [18] |
| MonoGS is permissively licensed. | Corrected | MonoGS is not permissive in the usual MIT/BSD/Apache sense; its license is a custom university/non-commercial/internal-academic research license. | [19], [20] |
| Gaussian-SLAM license is unknown. | Corrected | Gaussian-SLAM is MIT licensed according to GitHub metadata and its license file. | [21], [22] |
| Photo-SLAM license is unknown/permissive. | Corrected | Photo-SLAM is GPLv3 according to GitHub metadata and its license file; note third-party Gaussian Splatting components may have additional non-commercial INRIA terms. | [23], [24] |
| DiskChunGS license is permissive. | Corrected | DiskChunGS is not permissive. README/license evidence indicates GPLv3 plus a custom Gaussian-Splatting/non-commercial research license restriction. | [25], [26] |
| Gaussian-LIC license is unknown. | Corrected with caveat | Gaussian-LIC README states “The code is released under the GNU General Public License v3 (GPL-3).” GitHub does not detect a license and no root `LICENSE` file was found via GitHub API in this check, so cite the README wording and keep a caveat. | [27], [28] |

## License classification snapshot

| System | Public code status | License classification | Primary source evidence |
|---|---|---|---|
| SplaTAM | Full public repo | **Permissive: BSD-3-Clause** | [17], [18] |
| MonoGS / Gaussian Splatting SLAM | Full public repo | **Custom/non-commercial academic** | [19], [20] |
| Gaussian-SLAM | Full public repo | **Permissive: MIT** | [21], [22] |
| Photo-SLAM | Full public repo | **GPLv3**, plus third-party non-commercial terms caveat | [23], [24] |
| RTG-SLAM | Full public repo | **GPLv3** | [1], [2], [4] |
| GS-SLAM | Project page + modified rasterizer only found | **Rasterizer: custom/non-commercial academic**; full implementation license not applicable/not found | [5], [6], [7] |
| Google Splat-SLAM | Full public repo | **Permissive: Apache-2.0** | [14], [16] |
| Erik Sandström Splat-SLAM | Pointer repo; code moved to Google Research | No independent license detected in pointer repo; use Google repo license for implementation | [13], [14], [16] |
| DiskChunGS | Full public repo | **Non-permissive/research-only risk**: GPLv3 plus custom non-commercial Gaussian-Splatting license language | [25], [26] |
| Gaussian-LIC | Full public repo | **GPLv3 per README**, GitHub license metadata unknown/null | [27], [28] |
| VIGS-SLAM | Project page code link inaccessible; separate repo with code withheld | Unknown | [8], [10], [11] |
| VINGS-Mono | Full public repo | Unknown/no license detected | [9], [12] |

## Dead, inaccessible, or likely hallucinated sources

- `https://github.com/cvg/vigs-slam` is linked from the VIGS-SLAM project page but returns **404 / Not Found** via GitHub API at the time of this check. Do not cite it as available code unless it becomes accessible. [8], [10]
- `ghPak1002/VIGS_SLAM` exists but is not usable as public implementation evidence: its README says source code and run instructions are temporarily withheld until paper acceptance. [11]
- A claim that GS-SLAM has a full implementation appears unsupported by the primary project page and repository found. Only project-page code and the modified rasterizer repository were confirmed. [5], [6], [7]
- A claim that Erik Sandström Splat-SLAM is a separate implementation from Google Splat-SLAM appears misleading. The Erik repository points to the Google Research repository. [13], [14]
- Gaussian-LIC’s license should not be inferred from GitHub license metadata because GitHub returns null/no detected license. Use the README statement and note the missing detected/root license-file caveat. [27], [28]

## Numbered sources

1. RTG-SLAM project page: https://gapszju.github.io/RTG-SLAM/
2. RTG-SLAM GitHub repo metadata: https://github.com/MisEty/RTG-SLAM
3. RTG-SLAM README: https://raw.githubusercontent.com/MisEty/RTG-SLAM/main/README.md
4. RTG-SLAM license: https://raw.githubusercontent.com/MisEty/RTG-SLAM/main/LICENSE
5. GS-SLAM project page: https://gs-slam.github.io/
6. GS-SLAM modified rasterizer repo metadata: https://github.com/yanchi-3dv/diff-gaussian-rasterization-for-gsslam
7. GS-SLAM modified rasterizer README/license: https://raw.githubusercontent.com/NPU-YanChi/diff-gaussian-rasterization-for-gsslam/main/README.md and https://raw.githubusercontent.com/yanchi-3dv/diff-gaussian-rasterization-for-gsslam/main/LICENSE.md
8. VIGS-SLAM project page: https://vigs-slam.github.io/
9. VINGS-Mono GitHub repo metadata: https://github.com/Fudan-MAGIC-Lab/VINGS-Mono
10. Inaccessible VIGS-SLAM code link: https://github.com/cvg/vigs-slam
11. VIGS_SLAM withheld-code repo: https://github.com/ghPak1002/VIGS_SLAM
12. VINGS-Mono README: https://raw.githubusercontent.com/Fudan-MAGIC-Lab/VINGS-Mono/main/README.md
13. Erik Sandström Splat-SLAM pointer repo/README: https://github.com/eriksandstroem/Splat-SLAM and https://raw.githubusercontent.com/eriksandstroem/Splat-SLAM/main/README.md
14. Google Research Splat-SLAM repo metadata: https://github.com/google-research/Splat-SLAM
15. Google Research Splat-SLAM README: https://raw.githubusercontent.com/google-research/Splat-SLAM/main/README.md
16. Google Research Splat-SLAM license: https://raw.githubusercontent.com/google-research/Splat-SLAM/main/LICENSE
17. SplaTAM repo metadata/README: https://github.com/spla-tam/SplaTAM and https://raw.githubusercontent.com/spla-tam/SplaTAM/main/README.md
18. SplaTAM license: https://raw.githubusercontent.com/spla-tam/SplaTAM/main/LICENSE
19. MonoGS repo metadata/README: https://github.com/muskie82/MonoGS and https://raw.githubusercontent.com/muskie82/MonoGS/main/README.md
20. MonoGS license: https://raw.githubusercontent.com/muskie82/MonoGS/main/LICENSE.md
21. Gaussian-SLAM repo metadata/README: https://github.com/VladimirYugay/Gaussian-SLAM and https://raw.githubusercontent.com/VladimirYugay/Gaussian-SLAM/main/README.md
22. Gaussian-SLAM license: https://raw.githubusercontent.com/VladimirYugay/Gaussian-SLAM/main/LICENSE
23. Photo-SLAM repo metadata/README: https://github.com/HuajianUP/Photo-SLAM and https://raw.githubusercontent.com/HuajianUP/Photo-SLAM/main/README.md
24. Photo-SLAM license: https://raw.githubusercontent.com/HuajianUP/Photo-SLAM/main/LICENSE
25. DiskChunGS repo metadata/README: https://github.com/leggedrobotics/DiskChunGS and https://raw.githubusercontent.com/leggedrobotics/DiskChunGS/main/README.md
26. DiskChunGS license: https://raw.githubusercontent.com/leggedrobotics/DiskChunGS/main/LICENSE.md
27. Gaussian-LIC repo metadata/README: https://github.com/APRIL-ZJU/Gaussian-LIC and https://raw.githubusercontent.com/APRIL-ZJU/Gaussian-LIC/master/README.md
28. Gaussian-LIC project page: https://xingxingzuo.github.io/gaussian_lic/
