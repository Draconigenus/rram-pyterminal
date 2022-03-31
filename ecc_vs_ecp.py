
import numpy as np
import matplotlib.pyplot as plt

p1 = 0.002411
array1 = np.random.choice(a=[0, 1], p=[1 - p1, p1], replace=True, size=(256, 256))
p2 = 0.000244
array2 = np.random.choice(a=[0, 1], p=[1 - p2, p2], replace=True, size=(256, 256))
p3 = 0.33
array3 = np.random.choice(a=[0, 1], p=[1 - p3, p3], replace=True, size=(256, 256))

def plotECC():
	ECCs = np.array([
		[16, 6],
		[32, 7],
		[64, 8],
		[128, 9],
		[256, 10],
	])
	plt.figure(figsize=(5.0625, 2.6534))
	x = ECCs[:, 1] / (ECCs[:, 0] + ECCs[:, 1])
	x = np.append(x, 0)
	for rate, array in [[p1, array1], [p2, array2]]:
		fault = array.flatten()
		size = len(fault)
		yECC = np.zeros_like(x)
		for i, (data, parity) in enumerate(ECCs):
			chunk_size = data + parity
			for chunk_start in range(0, size, chunk_size):
				chunk_end = chunk_start + chunk_size
				fault_count = np.sum(fault[chunk_start:chunk_end])
				if (fault_count > 1): yECC[i] += fault_count
		# for i, overhead in enumerate(x): #simple whole module ECP table
		# 	fault = array.flatten()
		# 	fault_count = np.sum(fault)
		# 	ECP_correction_capacity = ((65536*overhead)-1)/17 #solcing equation of ECPn in section 3 of Schechter 2010 for n
		# 	yECP[i]=max(0, fault_count - ECP_correction_capacity)
		yECC = yECC / size
		yECC[-1] = rate
		plt.plot(x, yECC, marker= '.', label=f'Fault Rate: {rate * 100:.4f}%', antialiased=False)
	# plt.xticks(x, [str(ECC[0]) for ECC in ECCs])
	plt.xlim(0, max(x) + 0.01)
	plt.legend()
	# plt.show()
	plt.savefig("Plots/ECCFaultRate.png", dpi=2000)

def plotECP():
	ECPs = np.array(range(0,6))
	plt.figure(figsize=(5.0625, 2.6534))
	x = [(1 + ECP + ECP * np.log2(256))/256 for ECP in ECPs]
	x[0] = 0
	for rate, array in [[p1, array1], [p2, array2]]:
		yECP = np.zeros_like(ECPs)
		for i, ECP in enumerate(ECPs):
			for row in array:
				fault_count = np.sum(row)
				yECP[i] += max(0, fault_count - ECP)
		yECP = yECP / (256 ** 2)
		plt.plot(x, yECP, marker= '.', label=f'Fault Rate: {rate * 100:.4f}%', antialiased=False)
	plt.xlim(0, x[-1] + 0.005)
	plt.legend()
	# plt.show()
	plt.savefig("Plots/ECPFaultRate.png", dpi=2000)


if __name__=="__main__":
	plotECC()
	# plotECP()