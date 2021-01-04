import pandas as pd
import warnings
import os,sys

warnings.simplefilter("ignore") #IGNORE invalid pandas warnings

def preprocess_df(df:pd.DataFrame):

    """
    Preprocess the data as follows:
        Remove all entries where no I/O is occurring
        Create a score for total bytes
        Create a score for randomness
    """

    #Select all entries where I/O occurs
    df = df[
        df.TOTAL_BYTES_READ +
        df.TOTAL_BYTES_WRITTEN +
        df.TOTAL_MPIIO_INDEP_READS + df.TOTAL_MPIIO_COLL_READS +
        df.TOTAL_MPIIO_SPLIT_READS + df.TOTAL_MPIIO_NB_READS +
        df.TOTAL_MPIIO_INDEP_WRITES + df.TOTAL_MPIIO_COLL_WRITES +
        df.TOTAL_MPIIO_SPLIT_WRITES + df.TOTAL_MPIIO_NB_WRITES
        != 0
    ]

    #Select all entries with positive READ/WRITE/META Times
    df = df[
        (df.TOTAL_POSIX_F_READ_TIME >= 0) &
        (df.TOTAL_MPIIO_F_READ_TIME >= 0) &
        (df.TOTAL_POSIX_F_WRITE_TIME >= 0) &
        (df.TOTAL_MPIIO_F_WRITE_TIME >= 0) &
        (df.TOTAL_POSIX_F_META_TIME >= 0) &
        (df.TOTAL_MPIIO_F_META_TIME >= 0)
    ]


    #Get total amount of I/O (MB)
    df["TOTAL_IO"] = (df["TOTAL_BYTES_READ"] + df["TOTAL_BYTES_WRITTEN"])/(2**20)
    df["TOTAL_IO_PER_PROC"] = df["TOTAL_IO"]/df.NPROCS

    #Get total number of I/O ops
    df["TOTAL_READ_OPS"] = (
        df.TOTAL_POSIX_READS +
        df.TOTAL_STDIO_READS +
        df.TOTAL_MPIIO_INDEP_READS +
        df.TOTAL_MPIIO_COLL_READS +
        df.TOTAL_MPIIO_SPLIT_READS +
        df.TOTAL_MPIIO_NB_READS
    )
    df["TOTAL_WRITE_OPS"] = (
        df.TOTAL_POSIX_WRITES +
        df.TOTAL_STDIO_WRITES +
        df.TOTAL_MPIIO_INDEP_WRITES +
        df.TOTAL_MPIIO_COLL_WRITES +
        df.TOTAL_MPIIO_SPLIT_WRITES +
        df.TOTAL_MPIIO_NB_WRITES
    )
    df["TOTAL_IO_OPS"] = (df.TOTAL_READ_OPS + df.TOTAL_WRITE_OPS)

    #Total IO ops for varying sizes (fractional)
    df["TOTAL_SIZE_IO_0_100"] = (
        df.TOTAL_POSIX_SIZE_READ_0_100 +
        df.TOTAL_POSIX_SIZE_WRITE_0_100 +
        df.TOTAL_MPIIO_SIZE_READ_AGG_0_100 +
        df.TOTAL_MPIIO_SIZE_WRITE_AGG_0_100
    )/df.TOTAL_IO_OPS
    df["TOTAL_SIZE_IO_100_1K"] = (
        df.TOTAL_POSIX_SIZE_READ_100_1K +
        df.TOTAL_POSIX_SIZE_WRITE_100_1K +
        df.TOTAL_MPIIO_SIZE_READ_AGG_100_1K +
        df.TOTAL_MPIIO_SIZE_WRITE_AGG_100_1K
    )/df.TOTAL_IO_OPS
    df["TOTAL_SIZE_IO_1K_10K"] = (
        df.TOTAL_POSIX_SIZE_READ_1K_10K +
        df.TOTAL_POSIX_SIZE_WRITE_1K_10K +
        df.TOTAL_MPIIO_SIZE_READ_AGG_1K_10K +
        df.TOTAL_MPIIO_SIZE_WRITE_AGG_1K_10K
    )/df.TOTAL_IO_OPS
    df["TOTAL_SIZE_IO_10K_100K"] = (
        df.TOTAL_POSIX_SIZE_READ_10K_100K +
        df.TOTAL_POSIX_SIZE_WRITE_10K_100K +
        df.TOTAL_MPIIO_SIZE_READ_AGG_10K_100K +
        df.TOTAL_MPIIO_SIZE_WRITE_AGG_10K_100K
    )/df.TOTAL_IO_OPS
    df["TOTAL_SIZE_IO_100K_1M"] = (
        df.TOTAL_POSIX_SIZE_READ_100K_1M +
        df.TOTAL_POSIX_SIZE_WRITE_100K_1M +
        df.TOTAL_MPIIO_SIZE_READ_AGG_100K_1M +
        df.TOTAL_MPIIO_SIZE_WRITE_AGG_100K_1M
    )/df.TOTAL_IO_OPS
    df["TOTAL_SIZE_IO_0_1M"] = (
        df.TOTAL_SIZE_IO_0_100 +
        df.TOTAL_SIZE_IO_100_1K +
        df.TOTAL_SIZE_IO_100_1K +
        df.TOTAL_SIZE_IO_10K_100K +
        df.TOTAL_SIZE_IO_100K_1M
    )
    df["TOTAL_SIZE_IO_1M_4M"] = (
        df.TOTAL_POSIX_SIZE_READ_1M_4M +
        df.TOTAL_POSIX_SIZE_WRITE_1M_4M +
        df.TOTAL_MPIIO_SIZE_READ_AGG_1M_4M +
        df.TOTAL_MPIIO_SIZE_WRITE_AGG_1M_4M
    )/df.TOTAL_IO_OPS
    df["TOTAL_SIZE_IO_4M_10M"] = (
        df.TOTAL_POSIX_SIZE_READ_4M_10M +
        df.TOTAL_POSIX_SIZE_WRITE_4M_10M +
        df.TOTAL_MPIIO_SIZE_READ_AGG_4M_10M +
        df.TOTAL_MPIIO_SIZE_WRITE_AGG_4M_10M
    )/df.TOTAL_IO_OPS
    df["TOTAL_SIZE_IO_10M_100M"] = (
        df.TOTAL_POSIX_SIZE_READ_10M_100M +
        df.TOTAL_POSIX_SIZE_WRITE_10M_100M +
        df.TOTAL_MPIIO_SIZE_READ_AGG_10M_100M +
        df.TOTAL_MPIIO_SIZE_WRITE_AGG_10M_100M
    )/df.TOTAL_IO_OPS
    df["TOTAL_SIZE_IO_1M_100M"] = (
        df.TOTAL_SIZE_IO_1M_4M +
        df.TOTAL_SIZE_IO_4M_10M +
        df.TOTAL_SIZE_IO_10M_100M
    )
    df["TOTAL_SIZE_IO_100M_1G"] = (
        df.TOTAL_POSIX_SIZE_READ_100M_1G +
        df.TOTAL_POSIX_SIZE_WRITE_100M_1G +
        df.TOTAL_MPIIO_SIZE_READ_AGG_100M_1G +
        df.TOTAL_MPIIO_SIZE_WRITE_AGG_100M_1G
    )/df.TOTAL_IO_OPS
    df["TOTAL_SIZE_IO_1G_PLUS"] = (
        df.TOTAL_POSIX_SIZE_READ_1G_PLUS +
        df.TOTAL_POSIX_SIZE_WRITE_1G_PLUS +
        df.TOTAL_MPIIO_SIZE_READ_AGG_1G_PLUS +
        df.TOTAL_MPIIO_SIZE_WRITE_AGG_1G_PLUS
    )/df.TOTAL_IO_OPS
    df["TOTAL_SIZE_IO_100M_PLUS"] = (
        df.TOTAL_SIZE_IO_100M_1G +
        df.TOTAL_SIZE_IO_1G_PLUS
    )

    #TOTAL NUMBER OF MEDATA OPERATIONS
    df["TOTAL_MD_OPS"] = (
        df.TOTAL_POSIX_OPENS +
        df.TOTAL_POSIX_READS +
        df.TOTAL_POSIX_WRITES +
        df.TOTAL_POSIX_SEEKS +
        df.TOTAL_POSIX_STATS +
        df.TOTAL_POSIX_MMAPS +
        df.TOTAL_POSIX_FSYNCS +
        df.TOTAL_POSIX_FDSYNCS +

        df.TOTAL_STDIO_OPENS +
        df.TOTAL_STDIO_READS +
        df.TOTAL_STDIO_WRITES +
        df.TOTAL_STDIO_SEEKS +

        df.TOTAL_MPIIO_SYNCS
    )

    #SCORE ACCESS PATTERN
    df["TOTAL_ACCESS_PATTERN_SCORE"] = (
        .25*(df.TOTAL_POSIX_CONSEC_READS + df.TOTAL_POSIX_CONSEC_WRITES + df.TOTAL_POSIX_RW_SWITCHES) +
        .25*(df.TOTAL_POSIX_MEM_NOT_ALIGNED + df.TOTAL_POSIX_FILE_NOT_ALIGNED) +
        .75*(df.TOTAL_POSIX_SEQ_READS + df.TOTAL_POSIX_SEQ_WRITES)
    )

    #GET TOTAL AMOUNT OF TIME SPENT IN I/O and REMOVE ALL ENTRIES WHERE THERE IS NO IO
    df["TOTAL_READ_TIME"] = (
        df.TOTAL_POSIX_F_READ_TIME +
        df.TOTAL_MPIIO_F_READ_TIME
    )
    df["TOTAL_WRITE_TIME"] = (
        df.TOTAL_POSIX_F_WRITE_TIME +
        df.TOTAL_MPIIO_F_WRITE_TIME
    )
    df["TOTAL_MD_TIME"] = (
        df.TOTAL_POSIX_F_META_TIME +
        df.TOTAL_MPIIO_F_META_TIME
    )
    df["TOTAL_IO_TIME"] = (
        df.TOTAL_READ_TIME +
        df.TOTAL_WRITE_TIME +
        df.TOTAL_MD_TIME
    )
    df = df[(df.TOTAL_IO_TIME > 0)]

    #GET THE BANDWIDTH (MB/s)
    df["TOTAL_BANDWIDTH"] = df.TOTAL_IO / (df.TOTAL_READ_TIME + df.TOTAL_WRITE_TIME)

    #GET THE MD THROUGHPUT (ops/sec)
    df["TOTAL_THROUGHPUT"] = df.TOTAL_MD_OPS / df.TOTAL_MD_TIME

    #Remove the top 25% of TOTAL_IO_TIMEs
    #thresh = df["TOTAL_IO_TIME"].quantile(q=.75)
    #df = df[df.TOTAL_IO_TIME <= thresh]
    return df

DATASET="datasets/dataset.csv"
df = pd.read_csv(DATASET)
df = preprocess_df(df)
df.to_csv("datasets/preprocessed_dataset.csv", index=False)
columns = pd.DataFrame(data=df.columns)
columns.to_csv("datasets/preprocessed_schema.csv", index=False, header=False)
