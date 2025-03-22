<?php
declare(strict_types = 1);

namespace Unshell;

use Unshell\Engine as Engine;

class Cli
{
    protected array $argv;
    protected array $env;

    public function __construct(array $argv, array $env)
    {
        $this->argv = $argv;
        $this->env = $env;
    }

    protected function help(): void
    {
        echo <<<EOL
        Execute script through unshell runtime

        Usage:
        unshell COMMAND [SCRIPT_PATH] [ARGS...]

        Commands:
        help      Print this help message
        run       run a script through unshell runtime

        EOL;
    }

    protected function exec(): void
    {
        try {
            // todo rest args not supported
            [,, $script_path] = $this->argv;
        } catch (\Throwable $e) {
            //throw $th;
            var_dump('foo', $e->getMessage()); // on tombe pas la
        }

        $this->resolveScript($script_path);
        script();
    }

    protected function resolveScript(string $script): Script // tODO ??
    {
        if(!@include_once($script)) {
            // $cross = Colors::red('✘');
            $cross = '✘';
            echo("{$cross} unshell: Invalid SCRIPT_PATH");

            throw new \Exception('todo');
        } else {
            require_once($script);
        }

        // try {
        //     require_once($script);
        // } catch (\Throwable $e) {
        //     //throw $th;
        //     var_dump('resolveScript', $e);
        // }
    }

    public function run(): void
    {
        [, $unshell_command] = $this->argv;

        switch ($unshell_command) {
            case 'help':
                $this->help();
                break;
            case 'run':
                $this->exec();
                break;
            default:
                $this->help();
                break;
        };
    }
}
