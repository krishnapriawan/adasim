
map_s <- function(str) {
	print(str)
	if ( is.na(str) || str == "adasim.algorithm.routing.AdaptiveRoutingAlgorithm" ) {
		"TrafficLookaheadRouting"
	} else {
		"PriorityRouting"
	}
}

plot_data <- function(file) {
	data <- read.table( paste(file, "csv", sep="."), header=T, sep=',')
	p <- tapply( data$Time, list(data$Hops, data$Strategy) , mean)
	l <- levels(data$Strategy)
	print(l[1])
	pdf( paste(file, "pdf", sep=".") )
	barplot(t(p), beside=T, legend= c( map_s(l[1]) , map_s(l[2]) ), args.legend = list(x ='topright', bty='n', inset=c(-0.25,0)))
	dev.off()
}

plot_all_data <- function() {
	files <- list.files( path=".", pattern=".+.csv$" ) 
	for ( file in files) {
		s <- strsplit( file, ".csv" )
		plot_time_data(s)
	}
}

plot_time_data <- function(file) {
	data <- read.table( paste(file, "csv", sep="."), header=T, sep=',')
	p <- tapply( data$Time, list(data$Cars, data$Strategy) , mean)
	l <- levels(data$Strategy)
	pdf( paste(file, "pdf", sep=".") )
	barplot(t(p), beside=T, 
		legend= c( map_s(l[1]) , map_s(l[2]) ), 
		xlab ="# of vehicles", 
		ylab = "mean travel time", 
		args.legend = list( x = "topleft", bty='n' ) )
	dev.off()
} 
