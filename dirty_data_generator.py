import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta


def dirty_data(df, missing_prob=0.1, cap_prob=0.2, date_alter_prob=0.5, random_seed=None, columns=None):
    if random_seed is not None:
        np.random.seed(random_seed)
        random.seed(random_seed)

    df_dirty = df.copy()

    for col in df_dirty[columns]:
        col_type = df_dirty[col].dtype

        for i in range(len(df_dirty)):
            value = df_dirty.loc[i, col]

            # Randomly introduce missing values
            if np.random.rand() < missing_prob:
                df_dirty.loc[i, col] = np.nan
                continue

            # Handle string type
            if pd.api.types.is_string_dtype(col_type) and pd.notnull(value):
                if np.random.rand() < cap_prob:
                    df_dirty.loc[i, col] = random_cap(value)

            # Handle datetime type
            elif pd.api.types.is_datetime64_any_dtype(col_type) and pd.notnull(value):
                if np.random.rand() < date_alter_prob:
                    df_dirty.loc[i, col] = randomize_datetime(value)

    return df_dirty


def random_cap(text):
    """Randomly change capitalization in a string."""
    modes = ['upper', 'lower', 'capitalize', 'title', 'swapcase']
    mode = random.choice(modes)
    return getattr(text, mode)()

def randomize_datetime(dt):
    """Randomly strip time or add random time to date."""
    if isinstance(dt, pd.Timestamp):
        # 50% chance to keep time, otherwise remove it
        if dt.hour == 0 and dt.minute == 0 and dt.second == 0:
            # Was just a date, so add time
            rand_time = timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
            return dt + rand_time
        else:
            # Had time, so remove it
            return dt.normalize()
    return dt

