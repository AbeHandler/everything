a <- read_csv("daily.csv") %>% filter(date=="20200816")
count <- a %>% select(state, positive)
system('wget https://raw.githubusercontent.com/jakevdp/data-USstates/master/state-population.csv -O pop.csv')
pop <- read_csv("pop.csv") %>% filter(ages=="total")

pop %>% left_join(count, by = c("state/region" = "state"))

z <- pop %>% left_join(count, by = c("state/region" = "state")) %>% filter(year=="2013")

system("wget https://raw.githubusercontent.com/CivilServiceUSA/us-governors/master/us-governors/data/us-governors.csv  -O gov.csv")

gov <- read_csv("gov.csv") %>% select("state_code", "party")

final <- z %>% select(`state/region`, population, positive)

with_gov = final %>% left_join(gov, by = c("state/region" = "state_code"))

big_max = 40000000
small_max = 10000000

p <- ggplot(with_gov) + geom_point(aes(x=population, y=positive, color = `party`)) + xlim(0, big_max)

p <-p + geom_text(aes(x=population, y=positive, label = `state/region`), hjust = -.5)
