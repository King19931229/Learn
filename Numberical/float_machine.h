#pragma once

struct FloatMachine
{
	static constexpr unsigned int sign_mask = 0x80000000; // 1 << 31
	static constexpr unsigned int fraction_mask = 0x7fffff; // ((1 << 23) - 1)
	static constexpr unsigned int exponent_mask = 0x7f800000; // ((1 << 8) - 1) << 23
	static constexpr unsigned int fraction_patch_bit = 0x800000; // 1 << 23;
	static constexpr unsigned int fraction_patch_high_bit = 0x1000000; // 1 << 24;
	static constexpr unsigned int exponent_patch = 0x7f; // (1 << 7) - 1

	static float FloatAdd(float a, float b)
	{
		unsigned int a_as_int = *reinterpret_cast<unsigned int*>(&a);
		unsigned int b_as_int = *reinterpret_cast<unsigned int*>(&b);

		unsigned int sign_a = (sign_mask & a_as_int) >> 31;
		unsigned int sign_b = (sign_mask & b_as_int) >> 31;

		unsigned int exponent_a = (exponent_mask & a_as_int) >> 23;
		unsigned int exponent_b = (exponent_mask & b_as_int) >> 23;

		unsigned int fraction_a = (fraction_mask & a_as_int) + fraction_patch_bit;
		unsigned int fraction_b = (fraction_mask & b_as_int) + fraction_patch_bit;

		if (exponent_a > exponent_b)
		{
			fraction_b = fraction_b >> (exponent_a - exponent_b);
			exponent_b = exponent_a;
		}
		else if (exponent_a < exponent_b)
		{
			fraction_a = fraction_a >> (exponent_b - exponent_a);
			exponent_a = exponent_b;
		}

		if (fraction_a > fraction_b)
		{
			if (sign_a != sign_b)
			{
				fraction_a = fraction_a - fraction_b;
			}
			else
			{
				sign_a = sign_b;
				fraction_a = fraction_b + fraction_a;
			}
		}
		else if (fraction_a < fraction_b)
		{
			if (sign_a != sign_b)
			{
				sign_a = sign_b;
				fraction_a = fraction_b - fraction_a;
			}
			else
			{
				fraction_a = fraction_a + fraction_b;
			}
		}
		else
		{
			if (sign_a != sign_b)
			{
				fraction_a = 0;
				exponent_a = 0;
			}
			else
			{
				fraction_a += fraction_b;
			}
		}

		// Right shift normailize
		if (fraction_a >= fraction_patch_high_bit)
		{
			fraction_a += (fraction_a & 1);
			fraction_a >>= 1;
			exponent_a += 1;
		}

		// Left shift normailize
		while (!(fraction_a & fraction_patch_bit))
		{
			fraction_a <<= 1;
			exponent_a -= 1;
		}

		a_as_int = (sign_a << 31) | (exponent_a << 23) | (fraction_a & fraction_mask);
		a = *reinterpret_cast<float*>(&a_as_int);
		return a;
	}

	static float FloatSub(float a, float b)
	{
		unsigned int b_as_int = *reinterpret_cast<unsigned int*>(&b);
		b_as_int ^= sign_mask;
		b = *reinterpret_cast<float*>(&b_as_int);
		return FloatAdd(a, b);
	}

	static float FloatMul(float a, float b)
	{
		unsigned int a_as_int = *reinterpret_cast<unsigned int*>(&a);
		unsigned int b_as_int = *reinterpret_cast<unsigned int*>(&b);

		unsigned int sign_a = (sign_mask & a_as_int) >> 31;
		unsigned int sign_b = (sign_mask & b_as_int) >> 31;

		unsigned int exponent_a = (exponent_mask & a_as_int) >> 23;
		unsigned int exponent_b = (exponent_mask & b_as_int) >> 23;

		unsigned int fraction_a = (fraction_mask & a_as_int) + fraction_patch_bit;
		unsigned int fraction_b = (fraction_mask & b_as_int) + fraction_patch_bit;

		exponent_a = exponent_a + exponent_b - exponent_patch;
		sign_a ^= sign_b;
		fraction_a = (unsigned int)(((unsigned long long)fraction_a * (unsigned long long)fraction_b) >> 23);

		// Right shift normailize
		while (fraction_a >= fraction_patch_high_bit)
		{
			fraction_a += (fraction_a & 1);
			fraction_a >>= 1;
			exponent_a += 1;
		}

		// Left shift normailize
		while (!(fraction_a & fraction_patch_bit))
		{
			fraction_a <<= 1;
			exponent_a -= 1;
		}

		a_as_int = (sign_a << 31) | (exponent_a << 23) | (fraction_a & fraction_mask);
		a = *reinterpret_cast<float*>(&a_as_int);
		return a;
	}

	static float FloatDiv(float a, float b)
	{
		unsigned int a_as_int = *reinterpret_cast<unsigned int*>(&a);
		unsigned int b_as_int = *reinterpret_cast<unsigned int*>(&b);

		unsigned int sign_a = (sign_mask & a_as_int) >> 31;
		unsigned int sign_b = (sign_mask & b_as_int) >> 31;

		unsigned int exponent_a = (exponent_mask & a_as_int) >> 23;
		unsigned int exponent_b = (exponent_mask & b_as_int) >> 23;

		unsigned int fraction_a = (fraction_mask & a_as_int) + fraction_patch_bit;
		unsigned int fraction_b = (fraction_mask & b_as_int) + fraction_patch_bit;

		exponent_a = exponent_a - exponent_b + exponent_patch;
		sign_a ^= sign_b;
		fraction_a = (unsigned int)(((unsigned long long)fraction_a << 23) / (unsigned long long)fraction_b);

		// Right shift normailize
		while (fraction_a >= fraction_patch_high_bit)
		{
			fraction_a += (fraction_a & 1);
			fraction_a >>= 1;
			exponent_a += 1;
		}

		// Left shift normailize
		while (!(fraction_a & fraction_patch_bit))
		{
			fraction_a <<= 1;
			exponent_a -= 1;
		}

		a_as_int = (sign_a << 31) | (exponent_a << 23) | (fraction_a & fraction_mask);
		a = *reinterpret_cast<float*>(&a_as_int);
		return a;
	}
};