import numpy as np
import matplotlib.pyplot as plt

# パラメータ設定
NUM_PARTICLES = 100  # パーティクルの数
WORLD_SIZE = 30      # 数直線の長さ
MOTION_NOISE = 0.1    # 移動で生じるばらつきの標準偏差
SENSOR_NOISE = 0.1    # 観測雑音の標準偏差

def initialize_particles(num_particles, initial_position, world_size):
    particles = np.full(num_particles, initial_position, dtype=np.float64)
    particles %= world_size  # 世界の範囲内に制限
    return particles


def motion_update(particles, movement, world_size):
    particles += movement + np.random.normal(0, MOTION_NOISE, len(particles))
    particles %= world_size  # 数直線の範囲内に収める
    return particles

def sensor_update(particles, sensor_position):
    # 各パーティクルの重みを計算
    weights = np.exp(-((particles - sensor_position) ** 2) / (2 * SENSOR_NOISE ** 2))
    weights += 1e-1000  # ゼロ除算回避用の微小値
    weights /= np.sum(weights)  # 正規化
    return weights

def resample_particles(particles, weights):
    indices = np.random.choice(range(len(particles)), size=len(particles), p=weights)
    return particles[indices]

def plot_particles(particles, weights, robot_position):
    plt.hist(particles, bins=50, weights=weights, alpha=0.5, label="Particles")
    plt.xlim(0, WORLD_SIZE)
    plt.xlabel('position')
    plt.ylabel('weights')
    plt.legend()
    plt.show()

def main():
    # 初期化
    robot_position = 0
    particles = initialize_particles(NUM_PARTICLES, robot_position, WORLD_SIZE)

    for step in range(10):  # 10ステップ動作
        print(f"# Step {step + 1}")
        movement = +1   # 右に1進む
        robot_position = (robot_position + movement) % WORLD_SIZE   # 移動

        particles = motion_update(particles, movement, WORLD_SIZE)  # 移動後のパーティクル更新

        sensor_position = robot_position + np.random.normal(0, SENSOR_NOISE)    # 観測

        weights = sensor_update(particles, sensor_position) # 観測値の反映

        print(f"robot position: {robot_position}")
        # 最も重みが大きいパーティクルを表示
        max_weight_index = np.argmax(weights)
        max_weight_particle = particles[max_weight_index]
        print(f"max weight particle: {max_weight_particle:.2f} (weight: {weights[max_weight_index]:.4f})")

        # リサンプリング
        particles = resample_particles(particles, weights)

        # プロット
        plot_particles(particles, weights, robot_position)

if __name__ == "__main__":
    main()
