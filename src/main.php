<?php

declare(strict_types=1);
require __DIR__ . '/../vendor/autoload.php';

// namespace Unshell;


use \Unshell\Cli;

$cli = new Cli($argv, getenv());

try {
    $cli->run();

    exit(0);
} catch (\Throwable $e) {
    exit(1);
}
