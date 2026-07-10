# Robot Gaussian SLAM Survey Citation Pack

This file provides BibTeX entries and citation guidance for the LaTeX survey in `research/slam-survey/` on multi-robot / multi-agent online Gaussian SLAM. The keys are intentionally stable and descriptive. Prefer the archival venue entry when available; cite code repositories separately only when discussing implementation availability, reproducibility, or licensing.

## 1. Primary BibTeX entries

### MAGiC-SLAM

Direct URLs:
- Paper / CVPR OpenAccess: https://openaccess.thecvf.com/content/CVPR2025/html/Yugay_MAGiC-SLAM_Multi-Agent_Gaussian_Globally_Consistent__SLAM_CVPR_2025_paper.html
- PDF: https://openaccess.thecvf.com/content/CVPR2025/papers/Yugay_MAGiC-SLAM_Multi-Agent_Gaussian_Globally_Consistent__SLAM_CVPR_2025_paper.pdf
- arXiv: https://arxiv.org/abs/2411.16785
- Code: https://github.com/VladimirYugay/MAGiC-SLAM
- Project page: https://vladimiryugay.github.io/magic_slam

```bibtex
@inproceedings{yugay2025magic_slam,
  title     = {{MAGiC-SLAM}: Multi-Agent Gaussian Globally Consistent {SLAM}},
  author    = {Yugay, Vladimir and Gevers, Theo and Oswald, Martin R.},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  pages     = {6741--6750},
  year      = {2025},
  url       = {https://openaccess.thecvf.com/content/CVPR2025/html/Yugay_MAGiC-SLAM_Multi-Agent_Gaussian_Globally_Consistent__SLAM_CVPR_2025_paper.html}
}

@misc{yugay2024magic_slam_arxiv,
  title         = {{MAGiC-SLAM}: Multi-Agent Gaussian Globally Consistent {SLAM}},
  author        = {Yugay, Vladimir and Gevers, Theo and Oswald, Martin R.},
  year          = {2024},
  eprint        = {2411.16785},
  archivePrefix = {arXiv},
  primaryClass  = {cs.CV},
  url           = {https://arxiv.org/abs/2411.16785}
}

@misc{yugay2025magic_slam_code,
  title        = {{MAGiC-SLAM} Code Repository},
  author       = {Yugay, Vladimir and contributors},
  year         = {2025},
  howpublished = {GitHub repository},
  url          = {https://github.com/VladimirYugay/MAGiC-SLAM},
  note         = {Public research code; repository license text is MIT with third-party Gaussian Splatting component caveats.}
}
```

### MAC-Ego3D

Direct URLs:
- arXiv: https://arxiv.org/abs/2412.09723
- Code: https://github.com/Xiaohao-Xu/MAC-Ego3D

```bibtex
@misc{xu2024mac_ego3d,
  title         = {{MAC-Ego3D}: Multi-Agent Gaussian Consensus for Real-Time Collaborative Ego-Motion and Photorealistic {3D} Reconstruction},
  author        = {Xu, Xiaohao and Xue, Feng and Zhao, Shibo and Pan, Yike and Scherer, Sebastian and Huang, Xiaonan},
  year          = {2024},
  eprint        = {2412.09723},
  archivePrefix = {arXiv},
  primaryClass  = {cs.CV},
  url           = {https://arxiv.org/abs/2412.09723}
}

@misc{xu2024mac_ego3d_code,
  title        = {{MAC-Ego3D} Code Repository},
  author       = {Xu, Xiaohao and contributors},
  year         = {2024},
  howpublished = {GitHub repository},
  url          = {https://github.com/Xiaohao-Xu/MAC-Ego3D},
  note         = {Public MIT-licensed code for collaborative ego-motion and Gaussian-map reconstruction.}
}
```

### CoKo-SLAM

Direct URLs:
- arXiv: https://arxiv.org/abs/2604.00804
- arXiv DOI: https://doi.org/10.48550/arXiv.2604.00804
- Code: https://github.com/lemonci/coko-slam
- Alternate clone URL from README: https://github.com/lemonci/Coko-SLAM.git

```bibtex
@misc{li2026coko_slam,
  title         = {Compact Keyframe-Optimized Multi-Agent Gaussian Splatting {SLAM}},
  author        = {Li, Monica M. Q. and Lajoie, Pierre-Yves and Liu, Jialiang and Beltrame, Giovanni},
  year          = {2026},
  eprint        = {2604.00804},
  archivePrefix = {arXiv},
  primaryClass  = {cs.RO},
  doi           = {10.48550/arXiv.2604.00804},
  url           = {https://arxiv.org/abs/2604.00804}
}

@misc{li2026coko_slam_code,
  title        = {{CoKo-SLAM} Code Repository},
  author       = {Li, Monica M. Q. and contributors},
  year         = {2026},
  howpublished = {GitHub repository},
  url          = {https://github.com/lemonci/coko-slam},
  note         = {Public research code; repository license text is MIT with third-party Gaussian Splatting component caveats. Published dependency instructions appear rough and should not be treated as reproducibility proof.}
}
```

### CoMA-SLAM

Direct URLs:
- AAAI page: https://ojs.aaai.org/index.php/AAAI/article/view/37283
- DOI: https://doi.org/10.1609/aaai.v40i4.37283
- Code: https://github.com/npu-chenlin/CoMA-SLAM

```bibtex
@inproceedings{chen2026coma_slam,
  title     = {{CoMA-SLAM}: Collaborative Multi-Agent Gaussian {SLAM} with Geometric Consistency},
  author    = {Chen, Lin and Su, Yongxin and Wang, Jvboxi and Han, Pengcheng and Xia, Zhenyu and Bu, Shuhui and Li, Kun and Hu, Boni and Meng, Shengqi and Wang, Guangming},
  booktitle = {Proceedings of the AAAI Conference on Artificial Intelligence},
  volume    = {40},
  number    = {4},
  pages     = {2922--2929},
  year      = {2026},
  doi       = {10.1609/aaai.v40i4.37283},
  url       = {https://ojs.aaai.org/index.php/AAAI/article/view/37283}
}

@misc{chen2026coma_slam_code,
  title        = {{CoMA-SLAM} Code Repository},
  author       = {Chen, Lin and contributors},
  year         = {2026},
  howpublished = {GitHub repository},
  url          = {https://github.com/npu-chenlin/CoMA-SLAM},
  note         = {Public repository observed, but no top-level license was found in the research pass; cite only for source availability, not as reusable code.}
}
```

### HAMMER

Direct URLs:
- arXiv: https://arxiv.org/abs/2501.14147
- Project page: http://hammer-project.github.io
- IEEE entry: https://ieeexplore.ieee.org/abstract/document/11018364/
- IEEE DOI from arXiv metadata: https://doi.org/10.1109/LRA.2025.3575235

```bibtex
@article{yu2025hammer,
  title   = {{HAMMER}: Heterogeneous, Multi-Robot Semantic Gaussian Splatting},
  author  = {Yu, Javier and Chen, Timothy and Schwager, Mac},
  journal = {IEEE Robotics and Automation Letters},
  year    = {2025},
  doi     = {10.1109/LRA.2025.3575235},
  url     = {https://arxiv.org/abs/2501.14147},
  note    = {IEEE metadata should be checked for final volume, issue, and page numbers before camera-ready submission.}
}

@misc{yu2025hammer_arxiv,
  title         = {{HAMMER}: Heterogeneous, Multi-Robot Semantic Gaussian Splatting},
  author        = {Yu, Javier and Chen, Timothy and Schwager, Mac},
  year          = {2025},
  eprint        = {2501.14147},
  archivePrefix = {arXiv},
  primaryClass  = {cs.RO},
  doi           = {10.48550/arXiv.2501.14147},
  url           = {https://arxiv.org/abs/2501.14147}
}

@misc{yu2025hammer_project,
  title        = {{HAMMER} Project Page},
  author       = {Yu, Javier and Chen, Timothy and Schwager, Mac},
  year         = {2025},
  howpublished = {Project website},
  url          = {http://hammer-project.github.io},
  note         = {Use for videos, deployment examples, and code-availability status; code was not public in the research pass.}
}
```

### GRAND-SLAM

Direct URLs:
- arXiv: https://arxiv.org/abs/2506.18885
- DBLP: https://dblp.org/rec/journals/ral/ThomasSRH25.html
- DOI: https://doi.org/10.1109/LRA.2025.3623026

```bibtex
@article{thomas2025grand_slam,
  title   = {{GRAND-SLAM}: Local Optimization for Globally Consistent Large-Scale Multi-Agent Gaussian {SLAM}},
  author  = {Thomas, Annika and Sonawalla, Aneesa and Rose, Alex and How, Jonathan P.},
  journal = {IEEE Robotics and Automation Letters},
  volume  = {10},
  number  = {12},
  pages   = {13129--13136},
  year    = {2025},
  doi     = {10.1109/LRA.2025.3623026},
  url     = {https://doi.org/10.1109/LRA.2025.3623026}
}

@misc{thomas2025grand_slam_arxiv,
  title         = {{GRAND-SLAM}: Local Optimization for Globally Consistent Large-Scale Multi-Agent Gaussian {SLAM}},
  author        = {Thomas, Annika and Sonawalla, Aneesa and Rose, Alex and How, Jonathan P.},
  year          = {2025},
  eprint        = {2506.18885},
  archivePrefix = {arXiv},
  primaryClass  = {cs.RO},
  doi           = {10.48550/arXiv.2506.18885},
  url           = {https://arxiv.org/abs/2506.18885}
}
```

### MAGS-SLAM

Direct URLs:
- arXiv: https://arxiv.org/abs/2605.10760
- Project page: https://mags-slam.github.io/
- Website source repository: https://github.com/mags-slam/mags-slam.github.io

```bibtex
@misc{cao2026mags_slam,
  title         = {{MAGS-SLAM}: Monocular Multi-Agent Gaussian Splatting {SLAM} for Geometrically and Photometrically Consistent Reconstruction},
  author        = {Cao, Zhihao and Shao, Qi and Zhai, Shuhao and Zhang, Jing and Nguyen, Anh and Huang, Baoru},
  year          = {2026},
  eprint        = {2605.10760},
  archivePrefix = {arXiv},
  primaryClass  = {cs.CV},
  url           = {https://arxiv.org/abs/2605.10760}
}

@misc{cao2026mags_slam_project,
  title        = {{MAGS-SLAM} Project Page},
  author       = {Cao, Zhihao and Shao, Qi and Zhai, Shuhao and Zhang, Jing and Nguyen, Anh and Huang, Baoru},
  year         = {2026},
  howpublished = {Project website},
  url          = {https://mags-slam.github.io/},
  note         = {Project page states code and data will be released upon acceptance; do not cite as public implementation evidence.}
}
```

## 2. Relevant datasets, benchmark sources, and baselines

### Kimera-Multi / Kimera-Multi-Data

Direct URLs:
- Dataset repository: https://github.com/MIT-SPARK/Kimera-Multi-Data
- arXiv: https://arxiv.org/abs/2304.04362

```bibtex
@misc{tian2023kimera_multi,
  title         = {Resilient and Distributed Multi-Robot Visual {SLAM}: Datasets, Experiments, and Lessons Learned},
  author        = {Tian, Yulun and Chang, Yun and Quang, Long and Schang, Arthur and Nieto-Granda, Carlos and How, Jonathan P. and Carlone, Luca},
  year          = {2023},
  eprint        = {2304.04362},
  archivePrefix = {arXiv},
  primaryClass  = {cs.RO},
  url           = {https://arxiv.org/abs/2304.04362}
}

@misc{mit_spark_kimera_multi_data,
  title        = {{Kimera-Multi-Data}: A Large-Scale Multi-Robot Dataset for Multi-Robot {SLAM}},
  author       = {{MIT SPARK Lab}},
  howpublished = {Dataset repository},
  url          = {https://github.com/MIT-SPARK/Kimera-Multi-Data},
  note         = {Use for dataset access and benchmark details; cite the associated arXiv paper for the scholarly reference.}
}
```

### ReplicaMultiagent / ReplicaMultiAgent

Direct URLs:
- Hugging Face dataset: https://huggingface.co/datasets/voviktyl/ReplicaMultiagent
- Base Replica dataset page: https://github.com/facebookresearch/Replica-Dataset

```bibtex
@misc{replica_multiagent_dataset,
  title        = {{ReplicaMultiagent} Dataset},
  author       = {{Yugay, Vladimir and dataset contributors}},
  howpublished = {Hugging Face dataset},
  url          = {https://huggingface.co/datasets/voviktyl/ReplicaMultiagent},
  note         = {Derived multi-agent benchmark used by MAGiC-SLAM and CoKo-SLAM; no canonical citation or license metadata was visible in the research pass. Prefer citing the system papers that define their exact splits.}
}

@inproceedings{straub2019replica,
  title     = {The {Replica} Dataset: A Digital Replica of Indoor Spaces},
  author    = {Straub, Julian and Whelan, Thomas and Ma, Lingni and Chen, Yufan and Wijmans, Erik and Green, Simon and Engel, Jesse and Mur-Artal, Raul and Ren, Carl and Verma, Shobhit and Clarkson, Anton and Yan, Ming and Budge, Brian and Yan, Yajie and Pan, Xiaqing and Yon, June and Zou, Yuyang and Leon, Kimberly and Carter, Nigel and Briales, Jesus and Gillingham, Tyler and Mueggler, Elias and Pesqueira, Luis and Savva, Manolis and Batra, Dhruv and Strasdat, Hauke and De Nardi, Renzo and Goesele, Michael and Lovegrove, Steven and Newcombe, Richard},
  booktitle = {arXiv preprint arXiv:1906.05797},
  year      = {2019},
  url       = {https://arxiv.org/abs/1906.05797}
}
```

Note: The Replica BibTeX above is included because ReplicaMultiagent is derived from Replica-style scenes, but the multi-agent split itself should not be treated as equivalent to the base dataset. If the paper text discusses exact multi-agent sequences, cite the specific system paper or dataset page as well.

### 7-Scenes and TUM RGB-D baselines

Direct URLs:
- 7-Scenes page: https://www.microsoft.com/en-us/research/project/rgb-d-dataset-7-scenes/
- TUM RGB-D page: https://cvg.cit.tum.de/data/datasets/rgbd-dataset

```bibtex
@inproceedings{shotton2013scene_coordinate_regression,
  title     = {Scene Coordinate Regression Forests for Camera Relocalization in {RGB-D} Images},
  author    = {Shotton, Jamie and Glocker, Ben and Zach, Christopher and Izadi, Shahram and Criminisi, Antonio and Fitzgibbon, Andrew},
  booktitle = {Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
  year      = {2013},
  url       = {https://www.microsoft.com/en-us/research/project/rgb-d-dataset-7-scenes/},
  note      = {Canonical 7-Scenes dataset citation; used by MAC-Ego3D as a real RGB-D benchmark.}
}

@inproceedings{sturm2012tum_rgbd,
  title     = {A Benchmark for the Evaluation of {RGB-D} {SLAM} Systems},
  author    = {Sturm, J{"u}rgen and Engelhard, Nikolas and Endres, Felix and Burgard, Wolfram and Cremers, Daniel},
  booktitle = {Proceedings of the IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)},
  year      = {2012},
  url       = {https://cvg.cit.tum.de/data/datasets/rgbd-dataset}
}
```

### Collaborative / non-Gaussian baselines often appearing in tables

Use these only when discussing baseline comparisons reported by the target papers. Do not frame them as Gaussian SLAM methods.

Direct URLs:
- CP-SLAM paper/search source should be verified from the specific target paper’s bibliography before final submission.
- Swarm-SLAM repository: https://github.com/MISTLab/Swarm-SLAM
- CCM-SLAM paper/source should be verified from the specific target paper’s bibliography before final submission.
- ORB-SLAM3 repository: https://github.com/UZ-SLAMLab/ORB_SLAM3

```bibtex
@misc{swarm_slam_code,
  title        = {{Swarm-SLAM} Code Repository},
  author       = {{MIST Lab}},
  howpublished = {GitHub repository},
  url          = {https://github.com/MISTLab/Swarm-SLAM},
  note         = {Collaborative SLAM baseline used in multi-agent Gaussian SLAM comparisons; not a Gaussian Splatting method.}
}

@article{campos2021orb_slam3,
  title   = {{ORB-SLAM3}: An Accurate Open-Source Library for Visual, Visual-Inertial, and Multi-Map {SLAM}},
  author  = {Campos, Carlos and Elvira, Richard and Rodr{\'i}guez, Juan J. G{\'o}mez and Montiel, Jos{\'e} M. M. and Tard{\'o}s, Juan D.},
  journal = {IEEE Transactions on Robotics},
  volume  = {37},
  number  = {6},
  pages   = {1874--1890},
  year    = {2021},
  doi     = {10.1109/TRO.2021.3075644},
  url     = {https://github.com/UZ-SLAMLab/ORB_SLAM3}
}
```

## 3. Which survey sections should cite which keys

| Survey section / claim type | Recommended keys | Notes |
|---|---|---|
| Definition of target class: multi-agent online Gaussian SLAM with shared/fused map | `yugay2025magic_slam`, `xu2024mac_ego3d`, `thomas2025grand_slam`, `li2026coko_slam`, `chen2026coma_slam`, `yu2025hammer`, `cao2026mags_slam` | Use this cluster to establish the 2024--2026 emergence of the target class. |
| Centralized agent/server Gaussian submap SLAM | `yugay2025magic_slam`, `li2026coko_slam` | MAGiC-SLAM is the mature public-code RGB-D baseline; CoKo-SLAM is the compact keyframe/submap communication variant. |
| Distributed or consensus-style Gaussian-map collaboration | `xu2024mac_ego3d`, `chen2026coma_slam` | MAC-Ego3D for intra/inter-agent Gaussian consensus; CoMA-SLAM for distributed multi-agent 2D Gaussian-surfel SLAM. |
| Large-scale / outdoor multi-agent Gaussian SLAM | `thomas2025grand_slam`, `tian2023kimera_multi` | Cite Kimera-Multi when discussing the outdoor six-agent benchmark source. |
| Heterogeneous robot teams and semantic Gaussian maps | `yu2025hammer`, `yu2025hammer_project` | Paper for method/metrics; project page for demonstrations and code-status statements. |
| RGB-only / monocular multi-agent Gaussian SLAM | `cao2026mags_slam`, `cao2026mags_slam_project` | Treat as provisional / arXiv-stage unless the final archival version is available. |
| Communication-efficient compact map updates | `li2026coko_slam`, `chen2026coma_slam`, `cao2026mags_slam`, `yu2025hammer` | CoKo and CoMA for compact/distributed claims; HAMMER for explicit bandwidth evidence; MAGS for claimed compact monocular summaries. |
| ReplicaMultiagent / Multi-agent Replica benchmark tables | `replica_multiagent_dataset`, plus the system keys whose tables are quoted | Do not cite only the dataset page for paper-specific splits; cite the system paper for exact metrics. |
| Kimera-Multi Outdoor benchmark | `tian2023kimera_multi`, `thomas2025grand_slam` | Dataset/source plus GRAND-SLAM evaluation. |
| Public implementation availability and reproducibility | `yugay2025magic_slam_code`, `xu2024mac_ego3d_code`, `li2026coko_slam_code`, `chen2026coma_slam_code` | Keep paper citations separate from repository/code citations. |
| Baseline comparison paragraphs | `swarm_slam_code`, `campos2021orb_slam3`, plus CP-SLAM / CCM-SLAM entries after verifying exact bibliography | Avoid implying these baselines are Gaussian Splatting SLAM unless the cited baseline actually is. |

## 4. Paper-only vs public-code citation notes

### Cite as paper + public code

- **MAGiC-SLAM**: cite `yugay2025magic_slam` for the method and results; cite `yugay2025magic_slam_code` only for source availability, implementation maturity, MIT text, and third-party caveats.
- **MAC-Ego3D**: cite `xu2024mac_ego3d` for method claims and benchmark numbers; cite `xu2024mac_ego3d_code` for public MIT implementation status.
- **CoKo-SLAM**: cite `li2026coko_slam` for the compact keyframe-optimized method; cite `li2026coko_slam_code` when discussing the author repository and reproducibility caveats.
- **CoMA-SLAM**: cite `chen2026coma_slam` for the AAAI paper; cite `chen2026coma_slam_code` only to note that a public repository exists but reuse is blocked/uncertain without a top-level license.

### Cite as paper-only or project-page evidence, not reusable code

- **HAMMER**: cite `yu2025hammer` or `yu2025hammer_arxiv` for method and metrics. Cite `yu2025hammer_project` for videos, project status, and the fact that code was not public during the research pass.
- **GRAND-SLAM**: cite `thomas2025grand_slam` for the archival RA-L paper and `thomas2025grand_slam_arxiv` if using arXiv HTML-extracted details. No public code repository was found.
- **MAGS-SLAM**: cite `cao2026mags_slam` for the arXiv paper and `cao2026mags_slam_project` for the code/data release promise. Do not describe it as open source unless an implementation repo appears.

### Dataset/baseline caution

- **ReplicaMultiagent**: no canonical citation or license was visible on the Hugging Face dataset page in this pass. Use `replica_multiagent_dataset` only as a URL-bearing dataset artifact, and cite each system paper for its exact split and evaluation protocol.
- **Kimera-Multi**: use `tian2023kimera_multi` as the scholarly citation and `mit_spark_kimera_multi_data` as the access URL.
- **7-Scenes / TUM RGB-D**: cite only when discussing benchmark context or MAC-Ego3D / CoKo single-agent-compatible evaluation settings; neither is inherently a multi-agent Gaussian SLAM benchmark.
- **CP-SLAM / CCM-SLAM**: verify the exact BibTeX from the primary system paper bibliography before final submission. They are important baselines but were not the focus of this citation pack.

## 5. Suggested LaTeX citation patterns

- First mention of the field cluster:
  - `\cite{yugay2025magic_slam,xu2024mac_ego3d,thomas2025grand_slam,li2026coko_slam,chen2026coma_slam,yu2025hammer,cao2026mags_slam}`
- Open-source implementation paragraph:
  - `\cite{yugay2025magic_slam_code,xu2024mac_ego3d_code,li2026coko_slam_code,chen2026coma_slam_code}`
- Centralized server/submap fusion paragraph:
  - `\cite{yugay2025magic_slam,li2026coko_slam}`
- Distributed consensus / distributed optimization paragraph:
  - `\cite{xu2024mac_ego3d,chen2026coma_slam}`
- Heterogeneous robot semantic mapping paragraph:
  - `\cite{yu2025hammer}`
- Outdoor large-scale evaluation paragraph:
  - `\cite{thomas2025grand_slam,tian2023kimera_multi}`
- RGB-only future direction paragraph:
  - `\cite{cao2026mags_slam}`
