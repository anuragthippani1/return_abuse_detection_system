import React, { useState } from 'react';
import {
    Box,
    Container,
    Grid,
    Paper,
    Typography,
    Card,
    CardContent,
    Slider,
    FormControl,
    InputLabel,
    Select,
    MenuItem,
} from '@mui/material';
import { DataGrid, GridColDef, GridPaginationModel } from '@mui/x-data-grid';
import { useQuery } from 'react-query';
import { returnCaseApi } from '../services/api';

import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer,
} from 'recharts';

// Define your ReturnCase interface based on your data
interface ReturnCase {
    _id: string;
    id: string; // for DataGrid row id
    customer_id: string;
    return_reason: string;
    risk_score: number;
    suspicion_score: number;
    product_category: string;
    action_taken: string;
    timestamp: string;
}

interface ReturnCasesResponse {
    cases: ReturnCase[];
    // any other fields you get from API like total count, etc.
}

interface Statistics {
    total_cases: number;
    avg_risk_score: number;

    avg_suspicion_score: number;
    low_risk_cases: number;
    medium_risk_cases: number;
    high_risk_cases: number;
}

interface StatisticsResponse {
    statistics: Statistics;
}

const Dashboard: React.FC = () => {
    const [filters, setFilters] = useState({
        page: 1,
        per_page: 10,
        min_score: 0,
        max_score: 100,
        product_category: '',
        action_taken: '',
    });

    const { data: casesData, isLoading: casesLoading, error: casesError } = useQuery<ReturnCasesResponse>(
        ['returnCases', filters],
        () =>
            returnCaseApi.getReturnCases(filters).then(data => ({
                ...data,
                cases: data.cases.map((item: ReturnCase) => ({ ...item, id: item._id })),
            }))
    );

    const { data: statsData, isLoading: statsLoading, error: statsError } = useQuery<StatisticsResponse>(
        'statistics',
        () => returnCaseApi.getStatistics()
    );
    


    const handleFilterChange = (field: keyof typeof filters, value: any) => {
        setFilters((prev) => ({ ...prev, [field]: value }));
    };

    const columns: GridColDef<ReturnCase>[] = [
        { field: 'customer_id', headerName: 'Customer ID', width: 130 },
        { field: 'return_reason', headerName: 'Return Reason', width: 200 },
        {
            field: 'risk_score',
            headerName: 'Risk Score',
            width: 130,
            renderCell: (params) => (
                <Box
                    sx={{
                        color:
                            params.value >= 70
                                ? 'error.main'
                                : params.value >= 30
                                ? 'warning.main'
                                : 'success.main',
                    }}
                >
                    {params.value.toFixed(1)}%
                </Box>
            ),
        },
        {
            field: 'suspicion_score',
            headerName: 'Suspicion Score',
            width: 130,
            renderCell: (params) => (
                <Box
                    sx={{
                        color:
                            params.value >= 0.7
                                ? 'error.main'
                                : params.value >= 0.3
                                ? 'warning.main'
                                : 'success.main',
                    }}
                >
                    {(params.value * 100).toFixed(1)}%
                </Box>
            ),
        },
        { field: 'product_category', headerName: 'Product Category', width: 150 },
        { field: 'action_taken', headerName: 'Action', width: 130 },
        {
            field: 'timestamp',
            headerName: 'Date',
            width: 180,
            valueFormatter: (params) => new Date(params.value as string).toLocaleString(),
        },
    ];

    const riskDistributionData = statsData?.statistics
        ? [
              { name: 'Low Risk', value: statsData.statistics.low_risk_cases },
              { name: 'Medium Risk', value: statsData.statistics.medium_risk_cases },
              { name: 'High Risk', value: statsData.statistics.high_risk_cases },
          ]
        : [];

    if (casesLoading || statsLoading) {
        return <Typography variant="h6">Loading...</Typography>;
    }

    if (casesError || statsError) {
        return (
            <Typography variant="h6" color="error">
                Error loading data
            </Typography>
        );
    }

    return (
        <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
            <Typography variant="h4" gutterBottom>
                Return Abuse Dashboard
            </Typography>
            <Grid container spacing={3}>
                <Grid item xs={12} md={3}>
                    <Card>
                        <CardContent>
                            <Typography color="textSecondary">Total Cases</Typography>
                            <Typography variant="h4">{statsData?.statistics.total_cases || 0}</Typography>
                        </CardContent>
                    </Card>
                </Grid>
                <Grid item xs={12} md={3}>
                    <Card>
                        <CardContent>
                            <Typography color="textSecondary">Average Risk Score</Typography>
                            <Typography variant="h4">
                                {(statsData?.statistics.avg_risk_score || 0).toFixed(1)}%
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>
                <Grid item xs={12} md={3}>
                    <Card>
                        <CardContent>
                            <Typography color="textSecondary">High Risk Cases</Typography>
                            <Typography variant="h4" color="error">
                                {statsData?.statistics.high_risk_cases || 0}
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>
                <Grid item xs={12} md={3}>
                    <Card>
                        <CardContent>
                            <Typography color="textSecondary">Average Suspicion Score</Typography>
                            <Typography variant="h4">
                                {(statsData?.statistics.avg_suspicion_score || 0).toFixed(2)}
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 2, height: 300 }}>
                        <Typography variant="h6">Risk Distribution</Typography>
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={riskDistributionData}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="name" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Bar dataKey="value" fill="#8884d8" />
                            </BarChart>
                        </ResponsiveContainer>
                    </Paper>
                </Grid>

                <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 2 }}>
                        <Typography variant="h6">Filters</Typography>
                        <Grid container spacing={2}>
                            <Grid item xs={12}>
                                <Typography>Risk Score Range</Typography>
                                <Slider
                                    value={[filters.min_score, filters.max_score]}
                                    onChange={(_, value) => {
                                        const [min, max] = value as number[];
                                        handleFilterChange('min_score', min);
                                        handleFilterChange('max_score', max);
                                    }}
                                    valueLabelDisplay="auto"
                                    min={0}
                                    max={100}
                                />
                            </Grid>
                            <Grid item xs={12} md={6}>
                                <FormControl fullWidth>
                                    <InputLabel>Product Category</InputLabel>
                                    <Select
                                        value={filters.product_category}
                                        onChange={(e) => handleFilterChange('product_category', e.target.value)}
                                        label="Product Category"
                                    >
                                        <MenuItem value="">All</MenuItem>
                                        <MenuItem value="Electronics">Electronics</MenuItem>
                                        <MenuItem value="Clothing">Clothing</MenuItem>
                                        <MenuItem value="Books">Books</MenuItem>
                                    </Select>
                                </FormControl>
                            </Grid>
                            <Grid item xs={12} md={6}>
                                <FormControl fullWidth>
                                    <InputLabel>Action Taken</InputLabel>
                                    <Select
                                        value={filters.action_taken}
                                        onChange={(e) => handleFilterChange('action_taken', e.target.value)}
                                        label="Action Taken"
                                    >
                                        <MenuItem value="">All</MenuItem>
                                        <MenuItem value="Approve">Approve</MenuItem>
                                        <MenuItem value="Flag">Flag</MenuItem>
                                        <MenuItem value="Escalate">Escalate</MenuItem>
                                    </Select>
                                </FormControl>
                            </Grid>
                        </Grid>
                    </Paper>
                </Grid>

                <Grid item xs={12}>
                    <Paper sx={{ p: 2 }}>
                        <DataGrid
                            rows={casesData?.cases || []}
                            columns={columns}
                            paginationMode="server"
                            paginationModel={{ page: filters.page - 1, pageSize: filters.per_page }}
                            onPaginationModelChange={(model: GridPaginationModel) => {
                                handleFilterChange('page', model.page + 1);
                                handleFilterChange('per_page', model.pageSize);
                            }}
                            pageSizeOptions={[5, 10, 25]}
                            checkboxSelection
                            disableRowSelectionOnClick
                            loading={casesLoading}
                            getRowId={(row) => `${row.customer_id}-${row.timestamp}`}
                        />
                    </Paper>
                </Grid>
            </Grid>
        </Container>
    );
};

export default Dashboard;
