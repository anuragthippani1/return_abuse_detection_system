import React, { useState, useMemo } from 'react';
import {
    Box,
    Container,
    Grid,
    Paper,
    Typography,
    Card,
    CardContent,
    Slider,
    MenuItem,
    Select,
    FormControl,
    InputLabel,
} from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { useQuery } from 'react-query';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { returnCaseApi } from '../services/api';

// Define your ReturnCase interface based on your data
interface ReturnCase {
    case_id?: string;
    customer_id: string;
    return_reason: string;
    risk_score: number;
    suspicion_score: number;
    product_category: string;
    action_taken: string;
    reported_at: string;
}

interface ReturnCasesResponse {
    cases: ReturnCase[];
    total: number;
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

const riskScoreMarks = [
    { value: 0, label: '0%' },
    { value: 100, label: '100%' },
];

const Dashboard: React.FC = () => {
    const { data: casesData, isLoading: casesLoading, error: casesError } = useQuery<ReturnCasesResponse>(
        'returnCases',
        () => returnCaseApi.getReturnCases({})
    );

    const { data: statsData, isLoading: statsLoading, error: statsError } = useQuery<StatisticsResponse>(
        'statistics',
        () => returnCaseApi.getStatistics()
    );

    // Filters
    const [riskRange, setRiskRange] = useState<number[]>([0, 100]);
    const [productCategory, setProductCategory] = useState('');
    const [actionTaken, setActionTaken] = useState('');

    // Unique product categories and actions for dropdowns
    const productCategories = useMemo(() => {
        const set = new Set<string>();
        casesData?.cases.forEach((c) => set.add(c.product_category));
        return Array.from(set);
    }, [casesData]);
    const actionTakenOptions = useMemo(() => {
        const set = new Set<string>();
        casesData?.cases.forEach((c) => set.add(c.action_taken));
        return Array.from(set);
    }, [casesData]);

    // Filtering logic
    const filteredCases = useMemo(() => {
        if (!casesData?.cases) return [];
        return casesData.cases.filter((c) => {
            const risk = c.risk_score * 100;
            const inRisk = risk >= riskRange[0] && risk <= riskRange[1];
            const inCategory = productCategory ? c.product_category === productCategory : true;
            const inAction = actionTaken ? c.action_taken === actionTaken : true;
            return inRisk && inCategory && inAction;
        });
    }, [casesData, riskRange, productCategory, actionTaken]);

    // Risk distribution chart data
    const riskDist = useMemo(() => {
        let low = 0, med = 0, high = 0;
        casesData?.cases.forEach((c) => {
            if (c.risk_score < 0.3) low++;
            else if (c.risk_score < 0.7) med++;
            else high++;
        });
        return [
            { name: 'Low Risk', value: low },
            { name: 'Medium Risk', value: med },
            { name: 'High Risk', value: high },
        ];
    }, [casesData]);

    const columns: GridColDef<ReturnCase>[] = [
        { field: 'customer_id', headerName: 'Customer ID', width: 130 },
        { field: 'return_reason', headerName: 'Return Reason', width: 160 },
        {
            field: 'risk_score',
            headerName: 'Risk Score',
            width: 120,
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
        {
            field: 'suspicion_score',
            headerName: 'Suspicion Score',
            width: 140,
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
            field: 'reported_at',
            headerName: 'Date',
            width: 180,
            valueFormatter: (params) => new Date(params.value as string).toLocaleString(),
        },
    ];

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
                                {((statsData?.statistics.avg_risk_score || 0) * 100).toFixed(1)}%
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
                                {((statsData?.statistics.avg_suspicion_score || 0) * 100).toFixed(2)}
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>

                {/* Risk Distribution Chart */}
                <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 2, height: 300 }}>
                        <Typography variant="h6">Risk Distribution</Typography>
                        <ResponsiveContainer width="100%" height="80%">
                            <BarChart data={riskDist} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
                                <XAxis dataKey="name" />
                                <YAxis allowDecimals={false} />
                                <Tooltip />
                                <Bar dataKey="value" fill="#9575cd" barSize={40} />
                            </BarChart>
                        </ResponsiveContainer>
                    </Paper>
                </Grid>
                {/* Filters */}
                <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 2, height: 300 }}>
                        <Typography variant="h6">Filters</Typography>
                        <Box sx={{ mt: 2 }}>
                            <Typography gutterBottom>Risk Score Range</Typography>
                            <Slider
                                value={riskRange}
                                onChange={(_, v) => setRiskRange(v as number[])}
                                valueLabelDisplay="auto"
                                min={0}
                                max={100}
                                marks={riskScoreMarks}
                            />
                        </Box>
                        <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
                            <FormControl sx={{ minWidth: 160 }}>
                                <InputLabel>Product Category</InputLabel>
                                <Select
                                    value={productCategory}
                                    label="Product Category"
                                    onChange={(e) => setProductCategory(e.target.value)}
                                >
                                    <MenuItem value="">All</MenuItem>
                                    {productCategories.map((cat) => (
                                        <MenuItem key={cat} value={cat}>{cat}</MenuItem>
                                    ))}
                                </Select>
                            </FormControl>
                            <FormControl sx={{ minWidth: 160 }}>
                                <InputLabel>Action Taken</InputLabel>
                                <Select
                                    value={actionTaken}
                                    label="Action Taken"
                                    onChange={(e) => setActionTaken(e.target.value)}
                                >
                                    <MenuItem value="">All</MenuItem>
                                    {actionTakenOptions.map((act) => (
                                        <MenuItem key={act} value={act}>{act}</MenuItem>
                                    ))}
                                </Select>
                            </FormControl>
                        </Box>
                    </Paper>
                </Grid>

                {/* Data Table */}
                <Grid item xs={12}>
                    <Paper sx={{ p: 2 }}>
                        <DataGrid
                            rows={filteredCases}
                            columns={columns}
                            autoHeight
                            disableColumnMenu
                            disableRowSelectionOnClick
                            loading={casesLoading}
                            getRowId={(row) => row.case_id || row.customer_id + row.reported_at}
                        />
                    </Paper>
                </Grid>
            </Grid>
        </Container>
    );
};

export default Dashboard;
