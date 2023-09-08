# CFDBench

The code for the paper: [[upcoming] CFDBench: a comprehensive benchmark for data-driven methods for fluid dynamics](www.unknown.com).

## Data Generation

The directory `generation-code` contains the code for creating the mesh (ICEM code) and the schema code for batch generation in ANSYS Fluent.

> This part takes a lot of time, and you are better off just using our generated data instead.

## Data Interpolation

After generating data with numerical algorithms, it is then interpolated to a grid of 64x64. The raw data before interpolation is very large, and the below link is the interpolated data.

Main download link: [[click here]](https://cloud.tsinghua.edu.cn/d/435413b55dea434297d1/)

Contains 4 problems:

- `cavity`: Lid-driven cavity flow
- `tube`: Flow through a circular tube
- `dam`: Flow over a dam
- `cylinder`: Flow around a cylinder

> The cylinder flow is separated into three files because the file size exceeds the upload limit.

Each dataset includes 3 subsets, corresponding to changing BCs, domain geometries and physical properties.

The directory tree for the datasets:

```
▼ cavity/
    ▼ bc/
        ▼ case0000/
            ▼ u.npy
            ▼ v.npy
        ► case0001/
    ► geo/
    ► prop/
► tube/
► dam/
► cylinder/
```

The actual data for each velocity field is stored in `u.npy` and `v.npy`.

## Models

The basic types of models are autoregressive and non-autoregressive:

- Autoregressive:
    - Auto-FFN
    - Auto-DeepONet
    - Auto-EDeepONet
    - Auto-DeepONetCNN
    - ResNet
    - U-Net
    - FNO

- Non-autoregressive
    - FFN
    - DeepONet

The implementation of the models is located in `src/models`

## How to Run

### Prepare Data

Move the data into a `data` directory next to `src` directory, such that the directory
looks like:

```
▼ data/
    ▼ cavity/
        ▼ bc/
        ▼ geo/
        ▼ prop/
    ► tube/
    ► dam/
    ► cylinder/
► generation-code/
► src/
.gitignore
README.md
```

### Training

In the `src` directory, run `train.py` or `train_auto.py` to train non-autoregressive or autoregressive models respectively. Specify the model with `--model`. For example, run FNO on the cavity flow subset with all cases:

```bash
python train_auto.py --model fno --data cavity_prop_bc_geo
```

or, run DeepONet on the dam flow PROP + GEO subset:

```bash
python train.py --model deeponet --data dam_prop_geo
```

Results will be saved to `result/` directory by default, but can be customized with the `--output_dir` argument.

For more options, such as model hyperparameters, run `python train.py -h` or `python train_auto.py -h`.

### Inference

Set `--mode test` when executing `train.py` or `train_auto.py`.

### Hardware Requirements

See the Results section in the paper. Reduce the batch size if you run out of VRAM.