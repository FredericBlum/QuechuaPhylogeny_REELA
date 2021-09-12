library('ggplot2')
library('ggtree')
library('treeio')
library('RColorBrewer')
library('tidyverse')

## Lexicon

# SD-relax
#tree <- read.beast('../Models/models_lex/SD_Relax/crossandean_lex_01_sd.tree')

# BiCov-relax
tree <- read.beast('../Models/models_lex/BiCov_Relax/crossandean_lex_01_bicov_relax.tree')

# BiCov-strict
#tree <- read.beast('../Models/models_lex/BiCov_Strict/crossandean_lex_01_bicov_strict.tree')


tree@data['rposterior'] <- sprintf("%0.2f", as.numeric(tree@data[['posterior']]))
tree@data['rposterior'][tree@data['rposterior'] == 'NA',] <- NA

cls <- list(
    'Cuzqueño' = c("Curva", "Puno",
                   "Taquile", "Cuzco", "Maragua", "Pocona"),
    "Ayacuchano" = c("Ayacucho", "Arma", "Atalla"),
    "Apurimac" = "Apurimac",
    'Ecuadoriano' = c("Azuay", "Imbabura", "Troje", "Bobonaza", 
                      "Napo", "Serena", "Pastaza", "Putumayo"),
    'Chachapoyas' = c("Chachapoyas", "Lamas"),
    "Junín" = c("Pacaraos", "Tarma"),
    "Cajamarca" = c("Chetilla", "Inkawasi"),
    'Huanca' = c("Jauja", "Huanca"),
    "Ancash" = c("Chacpar", "Yanac", "Huallaga", "HuarazHuailas", "Raimondi", "Wari"),
    'Yauyos' = c("Apuri", "Huangascar", "SanPedro", "CacraHongos", "LinchaTana"),
    'Santiagueno' = "Santiagueno",
    'Laraos' = 'Laraos'
    
)


tree <- groupOTU(tree, cls, overlap="origin", connect=FALSE)

print(levels(attr(tree@phylo, 'group')))
colors <- c(
    "#333333", # 0  - i.e. non colored branches.
    
    brewer.pal(8, 'Oranges')[5], # Ancash
    brewer.pal(9, 'Greens')[6],  # Apurimac
    brewer.pal(9, 'Greens')[7], # Ayacucho
    brewer.pal(8, 'Oranges')[7], # Cajamarca
    brewer.pal(9, 'Greens')[9], # Chachapoyas
    brewer.pal(9, 'Greens')[5], # Cuzqueño
    brewer.pal(9, 'Greens')[7], # Ecuadoriano
    brewer.pal(8, 'Oranges')[8], # Huanca-Laraos
    brewer.pal(8, 'Oranges')[6], # Junín
    brewer.pal(6, 'Blues')[6],  # Laraos
    brewer.pal(9, 'Greens')[6],  # Santiagueno
    brewer.pal(6, 'Blues')[6]   # Yauyos
)


p <- ggtree(tree, aes(color=group), 
            ladderize=TRUE, size=1.5) %>% 
    revts()

p <- p + geom_tiplab(align=TRUE, linesize=2) +
    
    geom_label(aes(label=rposterior), 
               label.size=0.8, na.rm=TRUE, size=2.8,
               nudge_x=-0.2, nudge_y=0) +
    
    theme_tree2() +
    
    scale_color_manual(values=colors) +
    
    scale_x_continuous(breaks = seq(-20, 0, by = 2), 
                       # limits=c(-20, 7)) +  # sd model
                       limits = c(-8.7, 3)) +    # bicov models
    theme(legend.position="none")
col_idx = 2
for (clade in levels(attr(tree@phylo, 'group'))) {
    if (is.null(cls[[clade]])) next
    m <- MRCA(tree, cls[[clade]])
    if (!is.null(m)) {
        cat(paste(clade, m, col_idx, colors[col_idx]), "\n")
        p <- p + geom_cladelabel(
            node=m, label=clade, color = colors[col_idx],
            offset.text=0.3, # offset of text from labels
            extend=0.4, # extending the bars up/down
            
            #offset=4, # offset of label bars; sd
            offset = 1.8, # bicov

            barsize=2        )
    }
    col_idx <- col_idx + 1
}
p

ggsave('images/tree_lex_bicov_relaxed.png', p, width=10, height=10)
