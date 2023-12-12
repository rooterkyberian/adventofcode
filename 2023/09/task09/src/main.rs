use std::fs;

#[derive(Debug)]
struct Report {
    sequences: Vec<Vec<i32>>,
}

impl Report {
    fn new(data: &str) -> Report {
        let mut report = Vec::new();
        for line in data.trim().split("\n") {
            let numbers = line.split_whitespace()
                .map(|s| s.parse().unwrap())
                .collect();
            report.push(numbers);
        }
        return Report { sequences: report };
    }
}

fn calculate_next(sequence: &Vec<i32>) -> i32 {
    // create a new sequence based on difference between pairs from `sequence`
    let mut pyramid = Vec::new();
    pyramid.push(sequence.clone());
    // while last sequence has non-zero elements
    while pyramid.last().unwrap().iter().any(|&x| x != 0) {
        let last_sequence = pyramid.last().unwrap();
        let mut new_sequence = Vec::new();
        for pair in last_sequence.iter().zip(last_sequence.iter().skip(1)) {
            new_sequence.push(pair.1 - pair.0);
        }
        pyramid.push(new_sequence);
    }

    // pairwise reverse sequences from pyramid
    // from last to first sequence
    for i in (1..pyramid.len() - 1).rev() {
        let last_of_i = *pyramid[i].last().unwrap();
        let last_of_i_minus_1 = *pyramid[i - 1].last().unwrap();
        pyramid[i - 1].push(last_of_i + last_of_i_minus_1);
    }
    return pyramid[0].last().unwrap().clone();
}

fn calculate_prev(sequence: &Vec<i32>) -> i32 {
    // create a new sequence based on difference between pairs from `sequence`
    let mut pyramid = Vec::new();
    pyramid.push(sequence.clone());
    // while last sequence has non-zero elements
    while pyramid.last().unwrap().iter().any(|&x| x != 0) {
        let last_sequence = pyramid.last().unwrap();
        let mut new_sequence = Vec::new();
        for pair in last_sequence.iter().zip(last_sequence.iter().skip(1)) {
            new_sequence.push(pair.1 - pair.0);
        }
        pyramid.push(new_sequence);
    }

    // pairwise reverse sequences from pyramid
    // from last to first sequence
    for i in (1..pyramid.len() - 1).rev() {
        let last_of_super_seq = *pyramid[i].first().unwrap();
        let last_of_base = *pyramid[i - 1].first().unwrap();
        pyramid[i - 1].insert(0, last_of_base - last_of_super_seq);
    }
    return pyramid[0].first().unwrap().clone();
}

fn task1(report: &Report) -> i32 {
    let mut sum = 0;
    for sequence in report.sequences.iter() {
        sum += calculate_next(sequence);
    }
    return sum;
}

// Placeholder for task2
fn task2(report: &Report) -> i32 {
    let mut sum = 0;
    for sequence in report.sequences.iter() {
        sum += calculate_prev(sequence);
    }
    return sum;
}

fn main() {
    let example1 = "
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
";

    let report_example1 = Report::new(example1);

    let data = fs::read_to_string("../input.txt").expect("Unable to read file");
    let report_data = Report::new(&data);

    println!("task1(example1)= {:?}", task1(&report_example1));
    println!("task1(data)= {:?}", task1(&report_data));
    assert_eq!(task1(&report_example1), 114);
    assert_eq!(task1(&report_data), 1637452029);

    println!("task2(example1)= {:?}", task2(&report_example1));
    println!("task2(data)= {:?}", task2(&report_data));
    assert_eq!(task2(&report_example1), 114);
    assert_eq!(task2(&report_data), 1637452029);
}
