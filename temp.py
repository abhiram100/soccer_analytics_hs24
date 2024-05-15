import torch
import time

N = 4
N_pts = 1000
N_times = 100


def for_loop(indexes):
    grid_for = torch.zeros(N, N)
    # for loop
    for i in indexes:
        grid_for[i[0], i[1]] += 1
    return grid_for

def torch_method(indexes):
    grid_index_add = torch.zeros((indexes.size(0), N, N))
    grid_index_add[torch.arange(indexes.size(0)), indexes[:, 0], indexes[:, 1]] = 1
    grid_index_add = grid_index_add.sum(dim=0)
    return grid_index_add


indexes = torch.randint(0, N, (N_pts, 2))

st = time.time()
for _ in range(N_times):
    grid_for = for_loop(indexes)
en = time.time()
dt_for = en - st

# torch
st = time.time()
for _ in range(N_times):
    grid_index_add = torch_method(indexes)
en = time.time()
dt_torch = en - st

print(f"Check if for loop and torch give the same answer = {'PASS' if torch.equal(grid_for, grid_index_add) else 'FAIL'}")
print(f"\nTiming:")
print(f"\tfor loop: {dt_for*1e3} ms")
print(f"\ttorch: {dt_torch*1e3} ms")
print(f"\tSpeedup: {dt_for/dt_torch:.2f}x\n")