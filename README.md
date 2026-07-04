public double calculatePrice(ParkingStay parkingStay) {

    long minutes = ChronoUnit.MINUTES.between(
            parkingStay.getStartTime(),
            parkingStay.getEndTime()
    );

    long hours = (long) Math.ceil(minutes / 60.0);

    double price = 5.0
            + Math.max(0, hours - 1) * 4.0;

    double multiplier = Stream.of(
                    DayOfWeek.SATURDAY,
                    DayOfWeek.SUNDAY
            )
            .filter(day ->
                    day == parkingStay.getStartTime().getDayOfWeek())
            .map(day -> 0.5)
            .findFirst()
            .orElse(1.0);

    return price * multiplier;
}
