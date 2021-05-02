a <- read_csv("2021-05-02T0714_Grades-INFO_2301-001.csv")
b <- a["Final (1036622)"]
b <- b %>% rename("final" = "Final (1036622)") # syntax is new=old
ggplot(b, aes(x=final)) + geom_histogram(bins=15)  # no quote on column name

summary(b)