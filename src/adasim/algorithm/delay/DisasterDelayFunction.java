package adasim.algorithm.delay;

public class DisasterDelayFunction implements TrafficDelayFunction {
/*
 * Returns the number of delay function when disaster happens
 * @see adasim.algorithm.delay.TrafficDelayFunction#getDelay(int, int, int)
 */
	
	@Override
	public int getDelay(int weight, int capacity, int number) {	
		return 0;
	}

}
