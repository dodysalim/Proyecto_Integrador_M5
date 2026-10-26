"""Fábrica de gráficos con un estilo común para todo el dashboard."""
import numpy as np
import pandas as pd
import plotly.express as px

from mlops_pipeline.src.dashboard import config as c

_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, system-ui, sans-serif", color=c.TEXT, size=12),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=c.MUTED)),
    hoverlabel=dict(bgcolor="#121B2A", bordercolor=c.REF_COLOR, font=dict(color=c.TEXT)),
)
_AXES = dict(gridcolor=c.GRID, zeroline=False, linecolor=c.GRID, tickfont=dict(color=c.MUTED))


def _style(fig, **layout):
    fig.update_layout(**{**_LAYOUT, **layout})
    fig.update_xaxes(**_AXES)
    fig.update_yaxes(**_AXES)
    return fig


def stacked(ref: pd.Series, curr: pd.Series, value: str = 'Valor', group: str = 'Dataset',
            names=("Referencia", "Actual")) -> pd.DataFrame:
    """Une referencia y actual en formato largo para graficar."""
    return pd.DataFrame({value: np.concatenate([ref, curr]), group: [names[0]] * len(ref) + [names[1]] * len(curr)})


def target_distribution(y_ref, y_curr):
    df = stacked(y_ref, y_curr, value='Clase')
    return _style(px.histogram(df, x="Clase", color="Dataset", barmode="group", text_auto=True,
                               color_discrete_map=c.DATASET_COLORS, template="plotly_dark"), bargap=0.3)


def ecdf(ref, curr):
    return _style(px.ecdf(stacked(ref, curr), x="Valor", color="Dataset",
                          color_discrete_map=c.DATASET_COLORS, template="plotly_dark"))


def violin(ref, curr):
    return _style(px.violin(stacked(ref, curr), x="Dataset", y="Valor", color="Dataset", box=True, points="all",
                            color_discrete_map=c.DATASET_COLORS, template="plotly_dark"))


def scatter_3d(df, x, y, z, color, title):
    fig = px.scatter_3d(df, x=x, y=y, z=z, color=color, title=title, opacity=0.7,
                        color_discrete_sequence=c.QUALITATIVE, template="plotly_dark")
    return _style(fig, margin=dict(l=0, r=0, b=0, t=30), height=500)


def category_proportions(df, var):
    fig = px.bar(df, x=var, y="Proporción", color="Dataset", barmode="group",
                 color_discrete_map=c.DATASET_COLORS, template="plotly_dark")
    fig.update_xaxes(type='category', categoryorder='total descending')
    return _style(fig)


def mini_histogram(df, title):
    fig = px.histogram(df, x="Val", color="Set", nbins=20, barmode="overlay", opacity=0.6,
                       color_discrete_map=c.DATASET_COLORS, template="plotly_dark")
    return _style(fig, title=dict(text=title, font=dict(size=11, color=c.MUTED)), showlegend=False,
                  margin=dict(l=0, r=0, t=30, b=0), height=150,
                  xaxis=dict(showticklabels=False, title=None), yaxis=dict(showticklabels=False, title=None))


def mini_categories(df):
    fig = px.bar(df, x="Cat", y="Prop", color="Set", barmode="group", text="Cat",
                 color_discrete_map=c.DATASET_COLORS, template="plotly_dark")
    fig.update_traces(textposition='inside', textfont=dict(size=9, color='#0B1220'))
    fig.update_xaxes(type='category', showticklabels=False, title=None)
    return _style(fig, showlegend=False, margin=dict(l=0, r=0, t=5, b=0), height=130,
                  yaxis=dict(showticklabels=False, title=None))


def importance(corrs: pd.Series):
    fig = px.bar(x=corrs.index, y=corrs.values, color=corrs.values, color_continuous_scale=c.SEQUENTIAL,
                 title="Ranking de Influencia Global", template="plotly_dark")
    return _style(fig, coloraxis_showscale=False)


def correlation_heatmap(corr):
    fig = px.imshow(corr, color_continuous_scale=c.DIVERGING, zmin=-1, zmax=1, template="plotly_dark")
    return _style(fig, height=400, margin=dict(l=0, r=0, t=30, b=0))
