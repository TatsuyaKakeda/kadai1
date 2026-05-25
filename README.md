# 2D Ising (Lightweight Metropolis Version)

この段階では、軽量版として以下を実装しています。

- 2次元強磁性イジング模型（Metropolis法）
- L=4,8 程度で短時間に動作
- エネルギー、磁化、比熱、磁化率の計算
- pytest による小さい L のユニットテスト

## 実行方法

```bash
python run_simulation.py
```

## テスト

```bash
pytest -q
```

## 主要ファイル

- `ising2d.py`: モデル実装と観測量計算
- `run_simulation.py`: 軽量実行スクリプト
- `tests/test_ising2d.py`: ユニットテスト
