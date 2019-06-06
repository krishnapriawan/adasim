package adasim.model;

import org.apache.log4j.Logger;

import adasim.algorithm.routing.RoutingAlgorithm;

public class PriorityVehicle extends Vehicle {
	protected PriorityVehicle(int id) {
		super(id);
		// TODO Auto-generated constructor stub
	}

	private RoadSegment start; //Starting position
	private RoadSegment end; //Destination position
	private RoadSegment currentNode; //Current position
	private RoutingAlgorithm cs; //Strategy the vehicle uses to traverse the graph
	private static Logger logger = Logger.getLogger(Vehicle.class);

	
	/**
	 * 
	 * @param caller
	 * @return The (possibly) filtered start node of the car
	 */
	public RoadSegment getStartNode( Class<?> caller ) {
		return filterValue(start, caller);
	}
	
	/**
	 * @return The unfiltered starting node for the vehicle
	 */
	@SuppressWarnings("unused")
	private RoadSegment getStartNode() {
		return start;
	}

	/**
	 * Setting the start node also resets the current node of the vehicle.
	 * This is intended only for initializing the car and should
	 * not be called more than once.
	 * 
	 * @param start the start to set
	 */
	public void setStartNode(RoadSegment start) {
		this.start = start;
		this.currentNode = start;
		//reset the strategy
		setStrategy(cs);
	}
	
	/**
	 * @param caller
	 * @return the (possibly) filtered target not of the vehicle
	 */
	public RoadSegment getEndNode( Class<?> caller ) {
		return filterValue(end, caller);
	}


	/**
	 * @return The ending node for the vehicle
	 */
	@SuppressWarnings("unused")
	private RoadSegment getEndNode() {
		return end;
	}

	/**
	 * @param end the end to set
	 */
	public void setEndNode(RoadSegment end) {
		this.end = end;
		//reset the strategy
		setStrategy(cs);
	}
	
	/**
	 * @param caller
	 * @return the (possibly) filtered current node of the vehicle
	 */
	public RoadSegment getCurrentPosition( Class<?> caller ) {
		return filterValue(end, caller);
	}

	/**
	 * @return The current node of the vehicle
	 */
	private RoadSegment getCurrentPosition() {
		return currentNode;
	}

	/**
	 * Sets the current position to the given variable c
	 */
	public void setCurrentPosition(RoadSegment c) {
		currentNode = c;
		if ( isFinished() ) {
			logger.info( "STOP: " + vehiclePosition() );
		}
	}

	/**
	 * @return the cs
	 */
	public RoutingAlgorithm getStrategy() {
		return cs;
	}

	/**
	 * @param cs the cs to set
	 */
	public void setStrategy(RoutingAlgorithm cs) {
		this.cs = cs;
		if ( cs != null ) {
			cs.setStartRoad(start);
			cs.setEndRoad(end);
			cs.setVehicle(this);
		}
	}

	/**
	 * @return the position of the car as a string
	 */
	public String vehiclePosition() {
		StringBuffer buf = new StringBuffer( "Vehicle: ");
		buf.append( getID() );
		buf.append(" At: " );
		buf.append( getCurrentPosition().getID() );
		return buf.toString();
	}

	/* (non-Javadoc)
	 * @see adasim.model.AdasimAgent#takeSimulationStep()
	 */
	@Override
	public void takeSimulationStep( long cycle ) {
	}
	
	/**
	 * Called by GraphNodes during the vehicle movement protocol.
	 * The Vehicle responds by calling moveTo() on its
	 * currentNode.
	 */
	public void move() {
		if (isFinished()) return;	//quick end if we are done
		
		RoadSegment nextNode = cs.getNextNode();
		if ( nextNode == null ) {
			getCurrentPosition().park(this);
		} else {
			logger.info( "MOVE: " + vehiclePosition() + " To: " + nextNode.getID() );
			currentNode.moveTo(nextNode, this);
		}		
	}

	/**
	 * A vehicle is finished when it either has reached its
	 * target node, or when the strategy can no longer compute
	 * a path to the target.
	 */
	public boolean isFinished() {
		return currentNode != null && currentNode.equals(end);
	}


}
