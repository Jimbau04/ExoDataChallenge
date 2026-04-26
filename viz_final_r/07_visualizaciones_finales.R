# ============================================================================
# ExoData Challenge 2026 — Visualizaciones Finales (R/ggplot2)
# ============================================================================
# Genera gráficas nivel publicación. Usa scattermore para nubes de puntos grandes.
# Entrada: exoplanets_labeled.csv | Salida: ../figures/*.png @ 300 dpi
# ============================================================================

library(ggplot2)
library(dplyr)
library(tidyr)
library(scales)
library(scattermore)

dir.create("../figures", showWarnings = FALSE)
theme_pub <- theme_minimal(base_size = 11) +
  theme(
    panel.grid.minor = element_blank(),
    panel.grid.major = element_line(linewidth = 0.2, color = "gray85"),
    plot.title = element_text(face = "bold", size = 13),
    plot.subtitle = element_text(size = 10, color = "gray40"),
    plot.caption = element_text(size = 8, color = "gray60"),
    legend.position = "bottom",
    legend.title = element_text(size = 9),
    legend.text = element_text(size = 8)
  )

cluster_colors <- c(
  "Sub-Neptunes"          = "#E69F00",
  "Super-Earths (multi)"  = "#56B4E9",
  "Cold/Warm Jupiters"    = "#009E73",
  "Mini-Neptunes"         = "#F0E442",
  "Puffy Neptunes"        = "#D55E00",
  "Earth-sized Rocky"     = "#CC79A7"
)
method_colors <- c(
  "Transit" = "#1f77b4", "Radial Velocity" = "#ff7f0e",
  "Microlensing" = "#2ca02c", "Imaging" = "#d62728",
  "Transit Timing Variations" = "#9467bd", "Other" = "#8c564b"
)

df <- read.csv("exoplanets_labeled.csv", stringsAsFactors = FALSE)
df$cluster_name <- factor(df$cluster_name, levels = names(cluster_colors))
df$method_group <- factor(df$method_group, levels = names(method_colors))
df_clust <- df %>% filter(!is.na(cluster))
cat(sprintf("Loaded: %d planets, %d with clusters\n", nrow(df), nrow(df_clust)))


# ═══════ 1. MASS-RADIUS DIAGRAM ═══════
cat("\n[1/8] Mass-Radius...")
R <- 10^seq(log10(0.3), log10(100), length.out = 500)
cl <- data.frame(
  R = rep(R, 3),
  M = c(R^(1/0.27), R^(1/0.33), R^(1/0.37)),
  Comp = rep(c("100% Rock", "50% H2O", "100% H2O"), each = 500)
)
p1 <- ggplot(df_clust, aes(x = pl_rade, y = pl_bmasse, color = cluster_name)) +
  geom_line(data = cl, aes(x = R, y = M, linetype = Comp), color = "gray50", linewidth = 0.5, alpha = 0.6) +
  geom_scattermore(pointsize = 1.2, alpha = 0.5) +
  annotate("point", x = 1, y = 1, color = "black", size = 3, shape = 1, stroke = 1.2) +
  annotate("text", x = 1, y = 1, label = "Earth", hjust = -0.3, vjust = -0.5, size = 3.5, fontface = "italic") +
  annotate("point", x = 11.2, y = 318, color = "black", size = 3, shape = 1, stroke = 1.2) +
  annotate("text", x = 11.2, y = 318, label = "Jupiter", hjust = -0.3, vjust = -0.5, size = 3.5, fontface = "italic") +
  scale_x_log10(breaks = c(0.3, 1, 3, 10, 30, 100)) + scale_y_log10(breaks = c(0.1, 1, 10, 100, 1000, 10000)) +
  scale_color_manual(values = cluster_colors) +
  scale_linetype_manual(values = c("100% Rock" = "dashed", "50% H2O" = "dotted", "100% H2O" = "dotdash")) +
  labs(title = "Mass–Radius Diagram of Exoplanets",
       subtitle = "5,610 planets from NASA Exoplanet Archive — colored by GMM cluster (n=6)",
       x = expression(Radius ~ (R[oplus])), y = expression(Mass ~ (M[oplus])),
       color = "Cluster", linetype = "Composition (Zeng & Sasselov 2016)",
       caption = "ExoData Challenge 2026") + theme_pub
ggsave("../figures/01_mass_radius.png", p1, width = 9, height = 7, dpi = 300)
cat(" ✓\n")


# ═══════ 2. UMAP PROJECTIONS ═══════
cat("[2/8] UMAP...")
p2a <- ggplot(df_clust, aes(x = umap_x, y = umap_y, color = cluster_name)) +
  geom_scattermore(pointsize = 1.2, alpha = 0.5) +
  scale_color_manual(values = cluster_colors) + coord_fixed() +
  labs(title = "UMAP Projection by Cluster", x = "UMAP 1", y = "UMAP 2", color = "Cluster") + theme_pub
p2b <- ggplot(df_clust, aes(x = umap_x, y = umap_y, color = method_group)) +
  geom_scattermore(pointsize = 1.2, alpha = 0.5) +
  scale_color_manual(values = method_colors) + coord_fixed() +
  labs(title = "UMAP Projection by Detection Method", x = "UMAP 1", y = "UMAP 2",
       color = "Detection", caption = "Transit bias visible in dense central region") + theme_pub
ggsave("../figures/02a_umap_clusters.png", p2a, width = 9, height = 7, dpi = 300)
ggsave("../figures/02b_umap_detection.png", p2b, width = 9, height = 7, dpi = 300)
cat(" ✓\n")


# ═══════ 3. PERIOD-RADIUS (Neptune Desert) ═══════
cat("[3/8] Period-Radius...")
p3 <- ggplot(df_clust, aes(x = pl_orbper, y = pl_rade, color = cluster_name)) +
  annotate("rect", xmin = 0.1, xmax = 3, ymin = 2, ymax = 4, fill = "gray80", alpha = 0.3) +
  annotate("text", x = 0.4, y = 3, label = "Neptune Desert", size = 3.5, fontface = "italic", color = "gray40") +
  geom_hline(yintercept = 1.8, linetype = "dashed", color = "gray40", linewidth = 0.5) +
  annotate("text", x = 30000, y = 1.6, label = "Fulton Gap (~1.8 R⊕)", size = 3, color = "gray40", hjust = 1) +
  geom_scattermore(pointsize = 1.2, alpha = 0.5) +
  scale_x_log10(breaks = c(0.1, 1, 10, 100, 1000, 10000, 1e5),
                labels = c("0.1","1","10","100","1k","10k","100k")) +
  scale_y_log10(breaks = c(0.3, 1, 3, 10, 30, 100)) +
  scale_color_manual(values = cluster_colors) +
  labs(title = "Period–Radius Diagram", subtitle = "Neptune Desert (2–4 R⊕, <3 days) — a genuine astrophysical gap",
       x = "Orbital Period (days)", y = expression(Radius ~ (R[oplus])), color = "Cluster") + theme_pub
ggsave("../figures/03_period_radius.png", p3, width = 9, height = 7, dpi = 300)
cat(" ✓\n")


# ═══════ 4. BOXPLOTS BY CLUSTER ═══════
cat("[4/8] Boxplots...")
box_vars <- df_clust %>%
  select(cluster_name, log_rade, log_dens, log_period, log_eqt, st_met, sy_pnum) %>%
  pivot_longer(-cluster_name, names_to = "variable", values_to = "value") %>%
  filter(!is.na(value))
vl <- c(log_rade="log(Radius)", log_dens="log(Density)", log_period="log(Period)",
        log_eqt="log(T_eq)", st_met="[Fe/H]", sy_pnum="Planets in System")
box_vars$vl <- factor(vl[box_vars$variable], levels = unname(vl))
p4 <- ggplot(box_vars, aes(x = cluster_name, y = value, fill = cluster_name)) +
  geom_boxplot(outlier.size = 0.3, outlier.alpha = 0.2, linewidth = 0.3) +
  facet_wrap(~ vl, scales = "free_y", ncol = 2) +
  scale_fill_manual(values = cluster_colors, guide = "none") +
  labs(title = "Feature Distributions by Cluster", x = NULL, y = NULL) + theme_pub +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 7))
ggsave("../figures/04_boxplots.png", p4, width = 10, height = 8, dpi = 300)
cat(" ✓\n")


# ═══════ 5. HABITABLE ZONE ═══════
cat("[5/8] Habitable Zone...")
hz <- df %>% filter(!is.na(pl_insol) & !is.na(pl_rade) & pl_insol > 0)
n_hz <- sum(hz$hz_flag == 1, na.rm = TRUE)
p5 <- ggplot(hz, aes(x = pl_insol, y = pl_rade)) +
  annotate("rect", xmin = 0.2, xmax = 1.7, ymin = -Inf, ymax = 2, fill = "#2ca02c", alpha = 0.08) +
  annotate("text", x = 0.6, y = 3.5, label = "Conservative\nHabitable Zone", size = 3.5, color = "#2ca02c", fontface = "italic") +
  geom_scattermore(data = filter(hz, hz_flag == 0), aes(color = "Other"), pointsize = 1.5, alpha = 0.15) +
  geom_point(data = filter(hz, hz_flag == 1), aes(color = "HZ Candidate"), size = 1.5, alpha = 0.9) +
  annotate("point", x = 1, y = 1, color = "black", size = 3, shape = 1, stroke = 1.2) +
  annotate("text", x = 1.1, y = 1.1, label = "Earth", size = 3.5, fontface = "italic", hjust = 0) +
  scale_x_log10(breaks = c(0.1, 0.2, 0.5, 1, 1.7, 5, 10, 100, 1000)) +
  scale_y_log10(breaks = c(0.3, 0.5, 1, 2, 5, 10, 30)) +
  scale_color_manual(values = c("HZ Candidate" = "#2ca02c", "Other" = "gray70")) +
  geom_vline(xintercept = c(0.2, 1.7), linetype = "dashed", color = "#2ca02c", alpha = 0.4) +
  geom_hline(yintercept = 2, linetype = "dashed", color = "#2ca02c", alpha = 0.4) +
  labs(title = "Habitable Zone Candidates", subtitle = sprintf("Conservative HZ: 0.2 ≤ S⊕ ≤ 1.7, R<2 R⊕, 200≤T≤320K — %d candidates", n_hz),
       x = expression(Insolation ~ (S[oplus])), y = expression(Radius ~ (R[oplus])), color = NULL) + theme_pub
ggsave("../figures/05_habitable_zone.png", p5, width = 9, height = 7, dpi = 300)
cat(" ✓\n")


# ═══════ 6. DETECTION METHOD BIAS ═══════
cat("[6/8] Detection Bias...")
p6a <- df %>% count(method_group) %>% mutate(pct = n / sum(n) * 100) %>%
  ggplot(aes(x = reorder(method_group, -n), y = n, fill = method_group)) +
  geom_col() + geom_text(aes(label = sprintf("%d (%.1f%%)", n, pct)), vjust = -0.1, size = 3) +
  scale_fill_manual(values = method_colors, guide = "none") +
  scale_y_continuous(expand = expansion(mult = c(0, 0.15))) +
  labs(title = "Detection Method Distribution", subtitle = "73.4% found by Transit", x = NULL, y = "Planets") + theme_pub
p6b <- df_clust %>% count(cluster_name, method_group) %>% group_by(cluster_name) %>%
  mutate(pct = n / sum(n) * 100) %>%
  ggplot(aes(x = cluster_name, y = pct, fill = method_group)) + geom_col() +
  scale_fill_manual(values = method_colors) +
  labs(title = "Detection Method by Cluster", x = NULL, y = "%", fill = "Method") + theme_pub +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 7))
ggsave("../figures/06a_detection_distribution.png", p6a, width = 8, height = 5, dpi = 300)
ggsave("../figures/06b_detection_by_cluster.png", p6b, width = 9, height = 5, dpi = 300)
cat(" ✓\n")


# ═══════ 7. CORRELATION HEATMAP ═══════
cat("[7/8] Correlation...")
cor_m <- cor(df_clust %>% select(log_rade, log_dens, log_period, log_eqt, st_met, sy_pnum) %>% na.omit())
cor_melt <- as.data.frame(as.table(cor_m)); names(cor_melt) <- c("V1","V2","Correlation")
p7 <- ggplot(cor_melt, aes(V1, V2, fill = Correlation)) + geom_tile(color = "white", linewidth = 0.5) +
  geom_text(aes(label = sprintf("%.2f", Correlation)), size = 3.5) +
  scale_fill_gradient2(low = "#2166ac", mid = "white", high = "#b2182b", midpoint = 0, limits = c(-1, 1)) +
  labs(title = "Feature Correlation Matrix", x = NULL, y = NULL, fill = "Pearson r") + coord_fixed() +
  theme_pub + theme(axis.text.x = element_text(angle = 45, hjust = 1))
ggsave("../figures/07_correlation_heatmap.png", p7, width = 7, height = 6, dpi = 300)
cat(" ✓\n")


# ═══════ 8. SUMMARY TABLE ═══════
cat("[8/8] Cluster Summary...")
summary_table <- df_clust %>%
  group_by(cluster_name) %>%
  summarise(
    N = n(),
    `Radius (R⊕)` = round(median(pl_rade), 2),
    `Mass (M⊕)` = round(median(pl_bmasse), 1),
    `Density (g/cm³)` = round(median(pl_dens_calc), 2),
    `Period (d)` = round(median(pl_orbper), 1),
    `T_eq (K)` = round(median(pl_eqt), 0),
    `[Fe/H]` = round(median(st_met), 3),
    `Planets/Sys` = round(median(sy_pnum), 0),
    .groups = "drop"
  ) %>% arrange(desc(N))
write.csv(summary_table, "../docs/cluster_taxonomy.csv", row.names = FALSE)
cat(" ✓\n")

# ── Final ──
cat("\n═══════════════════════════════════════\n")
cat("✅ 8 VISUALIZATIONS + TAXONOMY TABLE\n")
for (f in sort(list.files("../figures", pattern = "*.png"))) {
  info <- file.info(file.path("../figures", f))
  cat(sprintf("  %-42s %6d KB\n", f, round(info$size/1024)))
}
cat("  docs/cluster_taxonomy.csv\n")
