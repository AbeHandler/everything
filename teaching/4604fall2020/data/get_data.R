a <- read_csv("daily.csv") %>% filter(date=="20200816")
count <- a %>% select(state, positive)
system('wget https://raw.githubusercontent.com/jakevdp/data-USstates/master/state-population.csv -O pop.csv')
pop <- read_csv("pop.csv") %>% filter(ages=="total")

pop %>% left_join(count, by = c("state/region" = "state"))

z <- pop %>% left_join(count, by = c("state/region" = "state")) %>% filter(year=="2013")

final <- z %>% select(`state/region`, population, positive)

final