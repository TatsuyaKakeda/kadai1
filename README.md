# 2D Ising (Lightweight Metropolis Version)

この段階では、軽量版として以下を実装しています。

- 2次元強磁性イジング模型（Metropolis法）
- L=4,8 程度で短時間に動作（温度掃引デモは L=4,8,12）
- エネルギー、磁化、比熱、磁化率の計算
- pytest による小さい L のユニットテスト
- 1 MCS あたり時間の簡易ベンチマーク（Lスケーリング確認の準備）

## 実行方法

### 単一温度の軽量実行

```bash
python run_simulation.py
```

### 温度掃引（demo）

```bash
python sweep_temperature.py
```

（matplotlib がない環境では `--skip-plot` を指定）

```bash
python sweep_temperature.py --skip-plot
```

出力:
- `results/sweep_demo.csv`
- `results/tc_estimates_demo.csv`（磁化率ピーク・比熱ピーク由来の Tc(L)）
- `results/observables_demo.png`（observables vs T）

### 計算時間スケーリングのベンチマーク（demo）

```bash
python benchmark_scaling.py
```

（matplotlib がない環境では `--skip-plot` を指定）

```bash
python benchmark_scaling.py --skip-plot
```

出力:
- `results/benchmark_demo.csv`
- `results/benchmark_demo_vs_L.png`
- `results/benchmark_demo_vs_L2.png`

## テスト

```bash
pytest -q
```

## 主要ファイル

- `ising2d.py`: モデル実装と観測量計算
- `run_simulation.py`: 単一温度の軽量実行スクリプト
- `sweep_temperature.py`: 複数温度の掃引、CSV保存、Tc(L)推定、プロット生成
- `analysis.py`: Tc(L)推定（ピーク法）と可視化
- `benchmark_scaling.py`: 1MCS時間の L 依存ベンチマーク
- `tests/test_ising2d.py`: 既存ユニットテスト
- `tests/test_sweep_benchmark.py`: 掃引・推定・ベンチマークの追加テスト
